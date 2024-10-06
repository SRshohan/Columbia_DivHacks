import axios from "axios";
import qs from "qs";

export default async function spotifyAuthReq() {
    try {
        const params = {
            grant_type: 'client_credentials',
            client_id: "7854839d9a444c49b832b801957794c4",
            client_secret: "a0e0e7ccdea34b14810edd05957d701f",
        };

        const response = await axios.post(
            "https://accounts.spotify.com/api/token",
            qs.stringify(params),
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );

        return response.data.access_token;
    } catch (error) {
        console.error("Error fetching Spotify token:", error);
        throw error;
    }
}