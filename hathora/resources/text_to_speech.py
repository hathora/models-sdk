"""Text-to-Speech (TTS) resources"""

from typing import Optional, Union, Literal, Dict, Any
from pathlib import Path

from hathora.types import AudioFile, AudioResponse
from hathora._utils import prepare_audio_file
from hathora.exceptions import APIError, ValidationError


class TextToSpeech:
    """Handles text-to-speech synthesis"""

    # Model parameter specifications
    MODEL_PARAMS = {
        "kokoro": {
            "voice": {
                "type": "str",
                "default": "af_bella",
                "description": "Voice to use for synthesis"
            },
            "speed": {
                "type": "float",
                "default": 1.0,
                "description": "Speech speed multiplier (0.5 = half speed, 2.0 = double speed)"
            }
        },
        "resemble": {
            "audio_prompt": {
                "type": "AudioFile",
                "default": None,
                "description": "Reference audio file for voice cloning (optional)"
            },
            "exaggeration": {
                "type": "float",
                "default": 0.5,
                "description": "Emotional intensity, range 0.0-1.0"
            },
            "cfg_weight": {
                "type": "float",
                "default": 0.5,
                "description": "Adherence to reference voice, range 0.0-1.0"
            }
        }
    }

    def __init__(self, client):
        self._client = client
        # Different base URLs for different models
        self._kokoro_url = "https://app-01312daf-6e53-4b9d-a4ad-13039f35adc4.app.hathora.dev"
        self._resemble_url = "https://app-efbc8fe2-df55-4f96-bbe3-74f6ea9d986b.app.hathora.dev"

    @classmethod
    def get_model_parameters(cls, model: str) -> Dict[str, Dict[str, Any]]:
        """
        Get available parameters for a specific model.

        Args:
            model: Model name ("kokoro" or "resemble")

        Returns:
            Dictionary of parameter specifications

        Example:
            >>> params = TextToSpeech.get_model_parameters("kokoro")
            >>> for param_name, param_info in params.items():
            ...     print(f"{param_name}: {param_info['description']}")
            voice: Voice to use for synthesis
            speed: Speech speed multiplier (0.5 = half speed, 2.0 = double speed)
        """
        if model not in cls.MODEL_PARAMS:
            raise ValidationError(f"Unknown model: {model}. Available models: {', '.join(cls.MODEL_PARAMS.keys())}")
        return cls.MODEL_PARAMS[model]

    @classmethod
    def list_models(cls) -> list:
        """
        List all available TTS models.

        Returns:
            List of model names

        Example:
            >>> models = TextToSpeech.list_models()
            >>> print(models)
            ['kokoro', 'resemble']
        """
        return list(cls.MODEL_PARAMS.keys())

    def print_model_help(self, model: str) -> None:
        """
        Print helpful information about a model's parameters.

        Args:
            model: Model name ("kokoro" or "resemble")

        Example:
            >>> client = yapp.Yapp(api_key="your-api-key")
            >>> client.text_to_speech.print_model_help("kokoro")
            Model: kokoro
            Parameters:
              - voice (str, default='af_bella'): Voice to use for synthesis
              - speed (float, default=1.0): Speech speed multiplier (0.5 = half speed, 2.0 = double speed)
        """
        params = self.get_model_parameters(model)
        print(f"\nModel: {model}")
        print("Parameters:")
        for param_name, param_info in params.items():
            default = param_info['default']
            default_str = f"'{default}'" if isinstance(default, str) else default
            print(f"  - {param_name} ({param_info['type']}, default={default_str}): {param_info['description']}")
        print()

    def convert(
        self,
        model: Literal["kokoro", "resemble"],
        text: str,
        **kwargs,
    ) -> AudioResponse:
        """
        Convert text to speech using the specified model.

        This is a unified interface that routes to the appropriate model-specific endpoint.
        Each model has its own parameters - pass them as keyword arguments.

        Args:
            model: Which TTS model to use ("kokoro" or "resemble")
            text: The text to convert to speech
            **kwargs: Model-specific parameters:

                For "kokoro":
                    - voice (str, default="af_bella"): Voice to use for synthesis
                    - speed (float, default=1.0): Speech speed multiplier (0.5-2.0)

                For "resemble":
                    - audio_prompt (AudioFile, optional): Reference audio for voice cloning
                    - exaggeration (float, default=0.5): Emotional intensity (0.0-1.0)
                    - cfg_weight (float, default=0.5): Adherence to reference voice (0.0-1.0)

        Returns:
            AudioResponse containing the generated audio

        Examples:
            >>> # Kokoro model
            >>> client = yapp.Yapp(api_key="your-api-key")
            >>> response = client.text_to_speech.convert(
            ...     "kokoro",
            ...     "Hello world",
            ...     voice="af_bella",
            ...     speed=1.2
            ... )
            >>> response.save("output.wav")
            >>>
            >>> # ResembleAI model
            >>> response = client.text_to_speech.convert(
            ...     "resemble",
            ...     "Hello world",
            ...     exaggeration=0.7,
            ...     cfg_weight=0.6
            ... )
            >>> response.save("output.wav")
            >>>
            >>> # ResembleAI with voice cloning
            >>> response = client.text_to_speech.convert(
            ...     "resemble",
            ...     "Hello world",
            ...     audio_prompt="reference.wav",
            ...     cfg_weight=0.9
            ... )
            >>> response.save("cloned.wav")
        """
        if model == "kokoro":
            # Extract Kokoro-specific parameters
            voice = kwargs.pop("voice", "af_bella")
            speed = kwargs.pop("speed", 1.0)

            # Warn if unknown parameters are passed
            if kwargs:
                unknown = ", ".join(kwargs.keys())
                valid_params = ", ".join(self.MODEL_PARAMS["kokoro"].keys())
                raise ValidationError(
                    f"Unknown parameters for Kokoro model: {unknown}. "
                    f"Valid parameters: {valid_params}\n"
                    f"Use client.text_to_speech.print_model_help('kokoro') for more details."
                )

            return self.kokoro(text=text, voice=voice, speed=speed)

        elif model == "resemble":
            # Extract ResembleAI-specific parameters
            audio_prompt = kwargs.pop("audio_prompt", None)
            exaggeration = kwargs.pop("exaggeration", 0.5)
            cfg_weight = kwargs.pop("cfg_weight", 0.5)

            # Warn if unknown parameters are passed
            if kwargs:
                unknown = ", ".join(kwargs.keys())
                valid_params = ", ".join(self.MODEL_PARAMS["resemble"].keys())
                raise ValidationError(
                    f"Unknown parameters for ResembleAI model: {unknown}. "
                    f"Valid parameters: {valid_params}\n"
                    f"Use client.text_to_speech.print_model_help('resemble') for more details."
                )

            return self.resemble(
                text=text,
                audio_prompt=audio_prompt,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight
            )

        else:
            available_models = ", ".join(self.MODEL_PARAMS.keys())
            raise ValidationError(
                f"Unknown model: {model}. Available models: {available_models}\n"
                f"Use client.text_to_speech.list_models() to see all models."
            )

    def kokoro(
        self,
        text: str,
        voice: str = "af_bella",
        speed: float = 1.0,
    ) -> AudioResponse:
        """
        Generate speech using the Kokoro-82M model.

        Args:
            text: The text to convert to speech
            voice: Voice to use for synthesis (default: "af_bella")
            speed: Speech speed multiplier (default: 1.0)
                  - 0.5 = half speed
                  - 2.0 = double speed

        Returns:
            AudioResponse containing the generated audio

        Example:
            >>> client = yapp.Yapp(api_key="your-api-key")
            >>> response = client.text_to_speech.kokoro(
            ...     text="Hello world",
            ...     voice="af_bella",
            ...     speed=1.0
            ... )
            >>> response.save("output.wav")
        """
        # Prepare JSON payload
        data = {
            "text": text,
            "voice": voice,
            "speed": speed,
        }

        # Make the request
        response = self._client._request(
            method="POST",
            url=f"{self._kokoro_url}/synthesize",
            json=data,
            headers={"Content-Type": "application/json"},
        )

        # Return audio response
        if isinstance(response, bytes):
            return AudioResponse(content=response)
        else:
            raise APIError("Unexpected response format from Kokoro API")

    def resemble(
        self,
        text: str,
        audio_prompt: Optional[AudioFile] = None,
        exaggeration: float = 0.5,
        cfg_weight: float = 0.5,
    ) -> AudioResponse:
        """
        Generate speech using the ResembleAI Chatterbox model.

        This model supports voice cloning with an optional audio prompt.

        Args:
            text: The text to convert to speech
            audio_prompt: Optional reference audio file for voice cloning
                         Can be file path, Path object, file-like object, or bytes
            exaggeration: Controls emotional intensity (default: 0.5)
                         Range: 0.0 to 1.0
            cfg_weight: Controls adherence to reference voice (default: 0.5)
                       Range: 0.0 to 1.0

        Returns:
            AudioResponse containing the generated audio

        Example:
            >>> client = yapp.Yapp(api_key="your-api-key")
            >>> # Simple generation
            >>> response = client.text_to_speech.resemble(
            ...     text="Hello world",
            ...     exaggeration=0.7
            ... )
            >>> response.save("output.wav")
            >>>
            >>> # With voice cloning
            >>> response = client.text_to_speech.resemble(
            ...     text="Hello world",
            ...     audio_prompt="reference_voice.wav",
            ...     cfg_weight=0.8
            ... )
            >>> response.save("cloned_voice.wav")
        """
        # Prepare form data
        form_data = {
            "text": (None, text),
            "exaggeration": (None, str(exaggeration)),
            "cfg_weight": (None, str(cfg_weight)),
        }

        files_to_close = []

        try:
            # Add audio prompt if provided
            if audio_prompt is not None:
                file_obj, mime_type = prepare_audio_file(audio_prompt)
                form_data["audio_prompt"] = ("audio_prompt", file_obj, mime_type)
                if isinstance(audio_prompt, (str, Path)):
                    files_to_close.append(file_obj)

            # Make the request
            response = self._client._request(
                method="POST",
                url=f"{self._resemble_url}/v1/generate",
                files=form_data,
            )

            # Return audio response
            if isinstance(response, bytes):
                return AudioResponse(content=response)
            else:
                raise APIError("Unexpected response format from ResembleAI API")

        finally:
            # Close any files we opened
            for file_obj in files_to_close:
                if hasattr(file_obj, 'close'):
                    file_obj.close()
