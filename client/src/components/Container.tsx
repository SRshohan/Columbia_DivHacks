import { cn } from '@/lib/utils'

interface ContainerProps extends React.ComponentProps<"div"> {

}

const Container = ({ children, className, ...props }: ContainerProps) => {
    return (
        <div {...props} className={cn('', className)}>
            { children }
        </div>
    )
}

export default Container