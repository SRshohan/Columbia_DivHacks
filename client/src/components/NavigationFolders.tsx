"use client"
import Link from "next/link"
import { Button } from "./ui/button"
import { useState } from "react"

const NavigationFolders = () => {
    const folders = [{
        route: "/",
        name: "Home",
    }, {
        route: "/about",
        name: "About"
    }, {
        route: "/services",
        name: "Services"
    }]

    const [activeFolder, setActiveFolders] = useState('Home');

    return (
        <div className=" flex flex-row gap-2">
            {folders.map((folder, idx) => {
                return (
                    <Button 
                        key={idx} 
                        variant="outline" 
                        className={`${folder.name === activeFolder ? "bg-green-400" : "bg-white"}`} asChild
                        onClick={() => setActiveFolders(folder.name)}
                    >
                        <Link href={folder.route}>
                            {folder.name}
                        </Link>
                    </Button>
                )
            })}
        </div>
    )
}

export default NavigationFolders