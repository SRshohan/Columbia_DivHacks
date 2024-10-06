import axios from "axios";
import spotifyAuthReq from "./spotifyAuthReq";

export default async function spotifyRecReq(genre: string | undefined) {
    try {
        const token = await spotifyAuthReq();

        if (token && genre) {
            const recs = await axios.get(`https://api.spotify.com/v1/recommendations`, {
                params: {
                    seed_genres: genre,
                    seed_tracks: "0c6xIDDpzE81m2q797ordA",
                    seed_artists: "4NHQUGzhtTLFvgF5SZesLK"
                },
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            return recs.data;
        }
    } catch (error) {
        console.error("Error fetching Spotify recommendations:", error);
        throw error;
    }
}