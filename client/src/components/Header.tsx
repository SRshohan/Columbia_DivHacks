import Link from "next/link";
import Container from "./Container";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";
import NavigationFolders from "./NavigationFolders";

export default function Header() {

    return (
        <header>
            <Container>
                <div className='flex justify-between items-center py-5 px-8 border-b-2'>
                    <div className="flex-1 font-bold">
                        <Link href="/">Health Care App</Link>
                    </div>
                    <div className=" flex flex-0.5 flex-row gap-10">
                        <NavigationFolders />
                        <SignedOut>
                            <SignInButton />
                        </SignedOut>
                        <SignedIn>
                            <UserButton />
                        </SignedIn>
                    </div>
                </div>
            </Container>
        </header>
    )
}