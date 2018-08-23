/* ----------------------------
/*  Name: CVP Assistant
    Author: Ankit/Ravi/Harman/Sonu
    Version: 1.0
/* -------------------------- */
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

var startButton = document.getElementById("testButton");
var progressArea = document.getElementById("processArea");
var txt = document.getElementById('txt');

var phrase = 'veer ji';

function getTextFromSpeech() {
    startButton.src = "http://icons.iconarchive.com/icons/icons-land/vista-multimedia/128/Microphone-Pressed-icon.png";
    startButton.disabled = true;
    progressArea.textContent = 'Listening...';

    var grammar = '#JSGF V1.0; grammar phrase; public <phrase> = ' + phrase + ';';
    var recognition = new SpeechRecognition();
    var speechRecognitionList = new SpeechGrammarList();
    speechRecognitionList.addFromString(grammar, 1);
    recognition.grammars = speechRecognitionList;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    var speechResult;
    recognition.onresult = function (event) {
        speechResult = event.results[0][0].transcript;
        console.log('text received: ' + speechResult);

        console.log('Confidence: ' + event.results[0][0].confidence);
        console.log('making output call...');
        makeRestCall(speechResult);
        progressArea.textContent = 'Request Processed!';
    }

    recognition.onspeechend = function () {
        recognition.stop();
        startButton.disabled = false;
        startButton.textContent = 'Ask me again!';
        progressArea.textContent = 'done';
        startButton.src = "http://icons.iconarchive.com/icons/icons-land/vista-multimedia/128/Microphone-Disabled-icon.png";
    }

    recognition.onerror = function (event) {
        startButton.disabled = false;
        startButton.textContent = 'Ask me again!';
    }
}

function makeRestCall(speechResult) {
    console.log('speech result: ' + speechResult);
    var payload = {
        "request": speechResult
    };
    console.log(JSON.stringify(payload));
    console.log(JSON.parse(JSON.stringify(payload)));
    $.ajax({
        url: "http://us152.sjc.aristanetworks.com:5000/api/bot/runCmd",
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        //contentType: "application/json; charset=utf-8",
        data: JSON.stringify(payload),
        //data: payload,
        error: function (d) {
            console.log("error: " + JSON.stringify(d));
        },
        success: function (rawData) {
            // rawData = speechResult;
            // console.log("rawData:" + rawData);
            // //txt.value = rawData;
            var parsed = JSON.parse(JSON.stringify(rawData));
            txt.textContent = parsed.response.speech;
            makeSpeakCall(parsed.response.speech);
            if (!parsed) {
                console.log('bad request');
                return;
            }

            // invoke the output function here
            console.log(JSON.stringify(parsed));
        }
    });
}

startButton.addEventListener('click', getTextFromSpeech);

var synth = window.speechSynthesis;
// Default voice Veena
var defaultVoice = synth.getVoices()[0];

// var speakForm = document.getElementById('speakForm');
//var waitingMic = document.getElementById('waitingMic');

function startListening(event) {
    alert('clicked');
}

function makeSpeakCall(speech) {
    console.log('speak call made with ' + txt);
    console.log(txt);
    speak(speech);
    //speak(txt.value);
    //speak(rawData);
};

function speak(textToSpeak) {
    var speaker = new SpeechSynthesisUtterance(textToSpeak);
    speaker.voice = defaultVoice;
    speaker.pitch = 1;
    speaker.pitch = 1;
    synth.speak(speaker);

    //callback functions
    speaker.onend = function (event) {
        console.log(event);
    };

    speaker.onpause = function (event) {
        console.log(event);
    };

    speaker.onend = function (event) {
        console.log(event);
    };

    speaker.onerror = function (event) {
        alert(textToSpeak);
    };
}