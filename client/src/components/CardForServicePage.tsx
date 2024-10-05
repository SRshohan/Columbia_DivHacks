import Image, { StaticImageData } from "next/image"
import { Button } from "./ui/button";
import Link from "next/link";

interface CardForServicePageInterface {
    image: StaticImageData;
    description: string;
}

const CardForServicePage = ({ image, description }: CardForServicePageInterface) => {
    return (
        <div className=" flex flex-col items-center max-w-4xl h-max border-2 bg-white border-black p-5 gap-4">
            <div className=" flex-0.5">
                <Image src={image} alt="" className=" w-[250px] h-[250px]"/>
            </div>  

            <div className=" flex-0.5 justify-center items-center">
                <Button asChild className=" w-full h-full">
                    <Link href={'/services/chatbot'}>
                        {description}
                    </Link>
                </Button>
            </div>
        </div>
    )
}  

export default CardForServicePage