import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        # Use environment variable for base URL, default to localhost for development
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

    def withdraw(self, card_number, pin, amount):
        try:
            response = requests.post(
                f"{self.base_url}/atm/withdraw",
                json={"CardNumber": card_number, "Pin": pin, "Amount": amount},
                timeout=10,  # Set a 10-second timeout for the request
            )
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            data = response.json()
            logger.info(f"API response: {data}")

            if data.get("success"):
                if "data" in data:
                    return data["data"]  # Return the WithdrawalResponse data
                else:
                    logger.error("API response missing 'data' key in success case")
                    return {"error": "Invalid response: Missing data"}
            else:
                # Include error details if available
                error_message = data.get("message", "Unknown error")
                error_details = data.get("details", {})
                error = (
                    f"{error_message}: {error_details}"
                    if error_details
                    else error_message
                )
                logger.error(f"API error: {error}")
                return {"error": error}

        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return {"error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            return {"error": "Can’t connect to the server"}
        except requests.exceptions.JSONDecodeError:
            logger.error("Invalid JSON response")
            return {"error": "Invalid response from server"}
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            return {"error": f"Server error: {str(e)}"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}
