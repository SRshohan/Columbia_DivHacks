import { Root, Track } from "@/types/Types";
import Image from "next/image";
import { useState, useEffect } from "react";
import Image1 from "@/images/hackaton_1.png";
import { Button } from "./ui/button";
import { X } from "lucide-react";

const Player = ({ data }: { data: Track[] }) => {
    const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
    const [currentTrack, setCurrentTrack] = useState<Track | null>(null);
    const [closed, setClosed] = useState(false)

    useEffect(() => {
        if (data && data.length > 0) {
            setCurrentTrack(data[currentTrackIndex]);
        }
    }, [data, currentTrackIndex]);

    const goToPreviousTrack = () => {
        setCurrentTrackIndex((prevIndex) =>
            prevIndex === 0 ? data.length - 1 : prevIndex - 1
        );
    };

    const goToNextTrack = () => {
        setCurrentTrackIndex((prevIndex) =>
            prevIndex === data.length - 1 ? 0 : prevIndex + 1
        );
    };

    const handleClose = () => {
        setClosed(true);
    }

    if (!currentTrack) {
        return <div>No tracks available</div>;
    }

    if (closed) {
        return ;
    }

    return (
        <div className="flex flex-col fixed top-0 mt-20 ml-5 left-15 border-2 border-black items-center justify-center w-[350px] py-4">
            <button onClick={handleClose} className=" absolute right-0 top-0 text-black hover:text-gray-500">
                <X />
            </button>
            <Image
                src={Image1}
                alt={currentTrack.name}
                width={90}
                height={90}
            />
            <h2 className="mt-2">
                <a href={currentTrack.external_urls.spotify} target="_blank" rel="noopener noreferrer">
                    {currentTrack.name}
                </a>
            </h2>
            <p>{currentTrack.artists.map(artist => artist.name).join(', ')}</p>
            <audio controls className="mt-3">
                <source src={currentTrack.preview_url} type="audio/mpeg" />
                Your browser does not support the audio element.
            </audio>
            <div className="flex flex-row w-full justify-between px-7 mt-3">
                <Button onClick={goToPreviousTrack}>Previous</Button>
                <Button onClick={goToNextTrack}>Next</Button>
            </div>
        </div>
    );
};

export default Player;
