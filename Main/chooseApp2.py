import alsaaudio, wave, numpy
import speech_recognition as sr
import pyttsx

#consts
rate=44100
timePerRecord=100
tempPath='./temp.wav'
#speed consts for pyttssx
resultRate=120
errorRate=170


#init
r = sr.Recognizer()
engine = pyttsx.init()
#set talking speed:
engine.setProperty('rate',resultRate)
#set voice:
engine.setProperty('voice','english-us')

def recordAudio():
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,card='C320M')
	inp.setchannels(1)
	inp.setrate(rate)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	w = wave.open(tempPath, 'w')
	w.setnchannels(1)
	w.setsampwidth(2)
	w.setframerate(rate)

	count=0
	while count<timePerRecord:
		count=count+1
		l, data = inp.read()
		w.writeframes(data)
	w.close()



#expects to get a dicionary where key is a string which is the command, value is the callback function
# e.g appCommands={'info': infoCommand, 'save': saveCommand}
def voiceCommand(appCommands):
	found=False
	while (True):
		print "give command"
		recordAudio()
		with sr.WavFile(tempPath) as source: # use the default microphone as the audio source
			audio = r.record(source) # listen for the first phrase and extract it into audio data
		try:
			t=r.recognize(audio);
			val=appCommands[t];
			return val;
		except LookupError: # speech is unintelligible
			engine.setProperty('rate',errorRate)
			print "did not understand speech, please try again"
			engine.say("did not understand speech, please try again")
			engine.runAndWait()
			engine.setProperty('rate',resultRate)

