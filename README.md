# MedTranscribe AI

MedTranscribe AI is a powerful tool that transcribes doctor-patient conversations in real-time and provides AI-assisted insights to support healthcare professionals.

## Features

- Real-time speech-to-text transcription
- Speaker identification (Doctor vs. Client)
- AI-powered analysis of medical conversations
- User-friendly GUI interface

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- An OpenAI API key
- An Amazon Web Services (AWS) account with access to Amazon Transcribe

## Installation

1. Clone the repository and save to a directory of your choosing:

    ```markdown
    git clone https://github.com/alexe0336/MedTranscribe-AI.git
    cd MedTranscribeAI
    ```

2. Install the required dependencies:

    Inside of the directory you want type this command to download required dependencies:
        ```markdown
        pip install -r requirements.txt
        ```

3. Create a `.env` file in the project root and add your OpenAI API key:

    Example .env file (Replace with your own OpenAI API Key):

        OPENAI_API_KEY=sadfsadg234324sdfdf234234235sdfsdsg32453245
    
4. Configure your AWS credentials. You can do this by setting up the AWS CLI or by creating a `~/.aws/credentials` file.
    
    Example setup using .aws folder (Create config and credentials files inside of your .aws folder and fill them with the below information): 

        .aws
            -config
            -credentials

        Example inside of config file:

            [default]
            region = us-east-1

        Example inside of credentials file (Replace with your own AWS key_id and access_key):

            [default]
            aws_access_key_id = asdfsafsafer23423424 
            aws_secret_access_key = 2342342343242sdfasgdsfg2435324sgdg

## Usage

1. Run the program:
    While inside of the directory folder where you saved the github repo.
    **Remember the API's you are using cost money, meaning when you are transcribing and when you ASK AI that costs money.**
    Enter this command to run the program :
        ```markdown
        python program.py
        ```

2. In the GUI:
- Click "Start Transcription" to begin transcribing audio.
- Use the "Enter Prompt" field to specify questions for the AI.
- Click "Update Prompt" to set your question.
- Click "Ask AI" to get AI-generated insights based on the transcription.
- Click "Stop Transcription" to end the transcription process.

3. The transcription will be saved in `transcription.txt`, and you can view the AI responses in the GUI.

## Contributing

Contributions to MedTranscribe AI are welcome. Please feel free to submit a Pull Request.
