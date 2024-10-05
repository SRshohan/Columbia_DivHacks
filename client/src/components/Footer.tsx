import Container from "./Container";

export default function Footer() {
    return (
        <footer className=" mt-12 mb-8 absolute bottom-0 border-black bg-white border-t-2 w-full">
            <Container>
                <div className=" flex flex-row justify-between px-8">
                    <div className="flex flex-col gap-">
                        <p className=" text-sm">
                            Health Care App &copy; { new Date().getFullYear() }
                        </p>
                        <p className=" text-sm">
                        All rights are reserved
                    </p>
                    </div>
                    <p className=" text-sm">
                        Made with NextJS
                    </p>
                </div>
            </Container>
        </footer>
    )
}