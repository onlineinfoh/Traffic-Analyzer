
import Navbar from "@/components/Navbar";
import ParticleBackground from "@/components/ParticleBackground";
import Hero from "@/components/Hero";
import Features from "@/components/Features";

const Index = () => {
  return (
    <main className="min-h-screen relative overflow-hidden">
      <div className="absolute inset-0 bg-noise opacity-[0.015] pointer-events-none animate-noise" />
      <ParticleBackground />
      <div className="relative z-10">
        <Navbar />
        <Hero />
        <Features />
      </div>
    </main>
  );
};

export default Index;
