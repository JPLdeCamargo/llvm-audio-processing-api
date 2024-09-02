# WHISPER transcription api and client
* Local testing:
    - Running the api:
        - ```python3 manage.py runserver ```
    - Testing with the client:
        - ``` python3 client.py ```

## Known issues:
* Stopping the recording before the max stipulated time has been reach can crash the client.

## TODO:
* Add dockerfile.
* Add audio generation models.
* Add diferent models for both generating and transcribing sound.
* Try to get the semmantic embeddings out of the transcriptions instead of plain text.
