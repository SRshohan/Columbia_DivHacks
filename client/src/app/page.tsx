"use client"

import CardForHomePage from "@/components/CardForHomePage";
import HackatomImage1 from '../images/hackaton_1.png'
import HackatomImage2 from '../images/hackaton_2.png'
import HackatomImage3 from '../images/hackaton_3.jpg'
import HackatomImage4 from '../images/hackaton_4.jpg'
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  const dummyData = [
    { image: HackatomImage1, question: "Feeling anxious today? Let's find a calm space together" },
    { image: HackatomImage2, question: "Having a tough day? We're here to listen and help" },
    { image: HackatomImage3, question: "Feeling overwhelmed? Let's break things down together" },
    { image: HackatomImage4, question: "Feeling alone? Remember, we're in this together." },
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % dummyData.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [dummyData.length]);

  const handleDotClick = (index: number) => {
    setCurrentIndex(index);
  };

  return (
    <main className="flex flex-col items-center justify-center bg-blue-300 min-h-screen p-4">
      <div className="flex flex-col items-center justify-center w-full h-full">
        {currentIndex + 1 !== dummyData.length ? (
                  <CardForHomePage image={dummyData[currentIndex].image} question={dummyData[currentIndex].question} />
        ) : (
          <Button asChild>
            <Link href="/services">
              Explore
            </Link>
          </Button>
        )}
        <div className="flex flex-row justify-between mt-4">
          {dummyData.map((_, index) => (
            <div
              key={index}
              className={`w-3 h-3 mx-1 rounded-full cursor-pointer ${currentIndex === index ? 'bg-black' : 'bg-gray-300'}`}
              onClick={() => handleDotClick(index)}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
