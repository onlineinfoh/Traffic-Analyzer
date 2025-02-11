
import { LineChart, Activity, Globe, Zap } from "lucide-react";

const features = [
  {
    icon: LineChart,
    title: "AI-Powered Traffic Predictions",
    description: "Leveraging a powerful Long Short-Term Memory (LSTM) machine learning model, our system predicts future traffic patterns with high accuracy."
  },
  {
    icon: Activity,
    title: "User-friendly Video Uploads",
    description: "Our intuitive interface allows users to easily upload traffic crossing videos, ensuring a smooth experience."
  },
  {
    icon: Globe,
    title: "Data Integration",
    description: "The platform continuously fetches and displays up-to-date traffic information, keeping users informed at all times."
  },
  {
    icon: Zap,
    title: "Modern Design",
    description: "The User Interface features a minimalist and dark-themed layout with crisp white sections for an aesthetically pleasing experience."
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
