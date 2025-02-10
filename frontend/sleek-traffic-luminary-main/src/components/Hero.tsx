
import { ArrowRight } from "lucide-react";

const Hero = () => {
  return (
    <div className="min-h-[80vh] flex items-center justify-center relative pt-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="space-y-8 animate-slide-up">
          <div className="inline-block">
            <span className="px-3 py-1 text-sm glass rounded-full animate-fade-in">
              Real-Time Analytics
            </span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight">
            Analyze Your Traffic with
            <span className="text-primary block mt-2">
              Unmatched Precision
            </span>
          </h1>

          <p className="text-muted-foreground text-lg sm:text-xl max-w-2xl mx-auto animate-fade-in">
            Real-time traffic analysis powered by advanced AI. Get deep insights into your traffic patterns, user behavior, and conversion metrics.
          </p>

          <div className="flex justify-center">
            <button className="btn-primary flex items-center justify-center gap-2 group">
              Upload
              <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
