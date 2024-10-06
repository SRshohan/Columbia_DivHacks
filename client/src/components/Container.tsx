import { cn } from '@/lib/utils'

const Container = ({ children, className, ...props }: React.ComponentProps<"div">) => {
    return (
        <div {...props} className={cn('', className)}>
            { children }
        </div>
    )
}

export default Container
