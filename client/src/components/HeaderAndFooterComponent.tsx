"use client"
import Footer from "./Footer";
import Header from "./Header";
import { usePathname } from "next/navigation";

const HeaderAndFooterComponent = () => {
    const pathname = usePathname()
    if (pathname !== '/services/chatbot')
    return (
        <div>
            <Header />
            <Footer />
        </div>
    )
}

export default HeaderAndFooterComponent