
import { LineChart, Activity, Globe, Zap } from "lucide-react";

const features = [
  {
    icon: LineChart,
    title: "Real-time Analytics",
    description: "Monitor your traffic in real-time with comprehensive analytics and insights."
  },
  {
    icon: Activity,
    title: "Performance Metrics",
    description: "Track key performance indicators and optimize your traffic flow."
  },
  {
    icon: Globe,
    title: "Global Coverage",
    description: "Analyze traffic patterns from anywhere in the world with our distributed network."
  },
  {
    icon: Zap,
    title: "Instant Insights",
    description: "Get immediate notifications and alerts about important traffic changes."
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
