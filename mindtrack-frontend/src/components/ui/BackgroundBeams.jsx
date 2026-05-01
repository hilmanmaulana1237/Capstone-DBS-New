import { cn } from "../../utils/cn";

export const BackgroundBeams = ({ className, lightMode = true }) => {
  return (
    <div
      className={cn(
        "absolute inset-0 z-0 flex items-center justify-center overflow-hidden",
        lightMode ? "bg-transparent" : "bg-slate-950",
        className
      )}
    >
      <div className={`absolute top-0 flex w-screen justify-center ${lightMode ? 'opacity-50' : 'opacity-30'}`}>
        {/* Glow Effects */}
        <div className={`h-[200px] w-[500px] blur-[100px] rounded-full mix-blend-screen ${lightMode ? 'bg-teal-200/40' : 'bg-indigo-500/30'}`} />
        <div className={`h-[300px] w-[300px] absolute top-[-100px] blur-[100px] rounded-full mix-blend-screen ${lightMode ? 'bg-emerald-200/30' : 'bg-cyan-400/20'}`} />
      </div>
      
      {/* Grid Pattern */}
      <div className={`absolute inset-0 bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] ${lightMode ? 'bg-[linear-gradient(to_right,#e2e8f0_1px,transparent_1px),linear-gradient(to_bottom,#e2e8f0_1px,transparent_1px)]' : 'bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)]'}`}></div>
    </div>
  );
};
