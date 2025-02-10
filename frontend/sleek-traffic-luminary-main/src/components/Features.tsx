
import { LineChart, Activity, Globe, Zap } from "lucide-react";

const features = [
  {
    icon: LineChart,
    title: "AI-Powered Traffic Predictions",
    description: "Our system uses a machine learning model to forecast traffic trends"
  },
  {
    icon: Activity,
    title: "Intuitive Video Uploads",
    description: "Users can upload traffic crossing videos through a user-friendly interface."
  },
  {
    icon: Globe,
    title: "Data Integration",
    description: "The platform fetches and displays up-to-date traffic information."
  },
  {
    icon: Zap,
    title: "Modern Design",
    description: "The UI features a sleek, dark-themed layout with clean white sections."
  }
];

const Features = () => {
  return (
    <section id="features" className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold">Powerful Features</h2>
          <p className="mt-4 text-muted-foreground">
            Everything you need to understand your traffic patterns
          </p>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="glass rounded-xl p-6 card-hover"
              style={{
                animationDelay: `${index * 100}ms`
              }}
            >
              <feature.icon className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
