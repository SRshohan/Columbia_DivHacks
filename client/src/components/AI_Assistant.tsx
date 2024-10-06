import spotifyRecReq from "@/app/requests/spotifyRecReq";
import { MessageSquare, X } from "lucide-react";
import { useState } from "react";
import Select from 'react-select';
import Player from "./Player";
import { Root, Track } from "@/types/Types";

const songGenres = [
    { value: "classical", label: "Classical" },
    { value: "country", label: "Country" },
    { value: "ambient", label: "Ambient" },
    { value: "instrumental", label: "Instrumental" },
    { value: "jazz", label: "Jazz" }
];

const AI_Assistant = () => {
    const [isOpen, setIsOpen] = useState(true);
    const [selectedGenre, setSelectedGenre] = useState<{ value: string; label: string } | null>(null);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [songs, setSongs] = useState<Track[]>([]);

    const handleClose = () => {
        setIsOpen(false);
    };

    const handleGenreChange = async (selectedOption: { value: string; label: string } | null) => {
        if (selectedOption) {
            setSelectedGenre(selectedOption);
            const response: Root = await spotifyRecReq(selectedOption.value);
            setSongs(response.tracks);
            console.log("songs ", response);
        }
    };

    const handleDropDownOpen = () => {
        setIsDropdownOpen(true);
    };

    const handleDropDownClose = () => {
        setIsDropdownOpen(false);
    };

    if (!isOpen) return null;

    return (
        <>
            <div className={`fixed ${isDropdownOpen ? 'bottom-32' : 'bottom-5'} right-10 w-80 bg-white shadow-lg p-4 transition-all duration-300`}>
                <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center">
                        <MessageSquare className="mr-2" />
                        <h2 className="text-lg font-semibold">AI Assistant</h2>
                    </div>
                    <button onClick={handleClose} className="text-gray-500 hover:text-gray-700">
                        <X />
                    </button>
                </div>
                <div className="mb-4 gap-2">
                    <p className="text-gray-700">Let&apos;s find something that can calm you down...</p>
                    <p className="text-gray-700">Which of the following musical genres do you prefer?</p>
                </div>
                <Select
                    value={selectedGenre}
                    onChange={handleGenreChange}
                    options={songGenres}
                    placeholder="Select a genre..."
                    className="w-full"
                    onMenuOpen={handleDropDownOpen}
                    onMenuClose={handleDropDownClose}
                    styles={{ menuPortal: base => ({ ...base, zIndex: 9999 }) }}
                    menuPlacement="auto"
                />
            </div>
            {selectedGenre && songs.length > 0 && (
                <Player data={songs} />
            )}
        </>
    );
};

export default AI_Assistant;
