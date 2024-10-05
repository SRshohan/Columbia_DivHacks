import CardForServicePage from "@/components/CardForServicePage";
import Hackaton5Image from '@/images/hackaton_5.jpg'

export default function ServicesPage() {
    return (
        <main className="flex items-center justify-center min-h-screen bg-blue-100 p-4">
            <div className=" flex flex-row gap-12">
                <CardForServicePage image={Hackaton5Image} description="Chat companion" />

                <CardForServicePage image={Hackaton5Image} description="Diagnoz analizer" />
            </div>
        </main>
    )
}