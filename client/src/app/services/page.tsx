// pages/services.tsx

import CardForServicePage from "@/components/CardForServicePage";
import Hackaton5Image from '@/images/hackaton_5.jpg';

export default function ServicesPage() {
    return (
        <main className="flex items-center justify-center min-h-screen animated-background p-4">
            <div className="flex flex-row gap-12">
                <CardForServicePage image={Hackaton5Image} description="Chat companion" />
                <CardForServicePage image={Hackaton5Image} description="Diagnoz analizer" />
            </div>
            <style>{`
                @keyframes gradientAnimation1 {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                @keyframes gradientAnimation2 {
                    0% { background-position: 100% 50%; }
                    50% { background-position: 0% 50%; }
                    100% { background-position: 100% 50%; }
                }

                .animated-background {
                    background: linear-gradient(270deg, #ff7e5f, #feb47b, #ff7e5f),
                                linear-gradient(90deg, #feb47b, #ff7e5f, #feb47b);
                    background-size: 600% 600%;
                    animation: gradientAnimation1 15s ease infinite,
                               gradientAnimation2 20s ease infinite;
                }
            `}</style>
        </main>
    )
}
