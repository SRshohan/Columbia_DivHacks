import Image, { StaticImageData } from "next/image";
import React from "react";

interface CardProps {
    image: StaticImageData;
    question: string;
}

const CardForHomePage: React.FC<CardProps> = ({ image, question }) => {
    return (
        <div className="flex flex-row items-center justify-center bg-white p-4 rounded-lg shadow-md w-full max-w-4xl h-[500px]">
            <div className="w-1/2 h-full relative">
                <Image
                    src={image}
                    alt="Card Image"
                    layout="fill"
                    objectFit="cover"
                    className="rounded-md"
                />
            </div>
            <div className="w-1/2 p-4 overflow-hidden">
                <p className="font-normal text-xl">{question}</p>
            </div>
        </div>
    );
};

export default CardForHomePage;
