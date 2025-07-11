import sys

sys.path.insert(0, "../")

import cppyy
from popsicle import START_JUCE_COMPONENT, juce

cppyy.cppdef("""
class AudioCallback : public juce::AudioIODeviceCallback
{
    void audioDeviceIOCallback(
        const float* const* inputChannelData,
        int numInputChannels,
        float* const* outputChannelData,
        int numOutputChannels,
        int numSamples,
        const juce::AudioIODeviceCallbackContext& context)
    {
        for (int channel = 0; channel < numOutputChannels; ++channel)
        {
            float* data = outputChannelData[channel];

            for (int sample = 0; sample < numSamples; ++sample)
                *data++ = rand() / (float)RAND_MAX;
        }
    }

    void audioDeviceAboutToStart(juce::AudioIODevice* device)
    {
    }

    void audioDeviceStopped()
    {
    }
};
""")


class MainContentComponent2(juce.Component):
    deviceManager = juce.AudioDeviceManager()
    audioCallback = cppyy.gbl.AudioCallback()

    def __init__(self):
        super().__init__()

        result = self.deviceManager.initialiseWithDefaultDevices(0, 2)
        if result.isNotEmpty():
            print(result.toRawUTF8())

        self.deviceManager.addAudioCallback(self.audioCallback)

        self.setSize(800, 600)

    def __del__(self):
        if not self.deviceManager:
            return

        self.deviceManager.removeAudioCallback(self.audioCallback)

        self.deviceManager.closeAudioDevice()
        self.deviceManager = None

    def paint(self, g):
        g.fillAll(juce.Colours.slategrey)


if __name__ == "__main__":
    START_JUCE_COMPONENT(MainContentComponent2, name="C++ Audio Callback")
