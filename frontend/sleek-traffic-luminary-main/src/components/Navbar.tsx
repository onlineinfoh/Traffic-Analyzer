
import { Menu, X } from "lucide-react";
import { useState, useEffect } from "react";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? "bg-background/80 backdrop-blur-lg" : ""
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <a href="/" className="text-xl font-bold">
              Traffic Analyzer
            </a>
          </div>

          <div className="hidden md:block">
            <div className="flex items-center space-x-4">
              <a href="#features" className="nav-item">
                Features
              </a>
              <button className="btn-primary">
                Upload
              </button>
            </div>
          </div>

          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md hover:bg-white/5"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        className={`${
          isOpen ? "translate-x-0" : "translate-x-full"
        } md:hidden fixed top-16 left-0 right-0 bottom-0 bg-background/95 backdrop-blur-lg transition-transform duration-300 ease-in-out`}
      >
        <div className="px-2 pt-2 pb-3 space-y-1">
          <a
            href="#features"
            className="block nav-item"
            onClick={() => setIsOpen(false)}
          >
            Features
          </a>
          <button
            className="w-full btn-primary mt-4"
            onClick={() => setIsOpen(false)}
          >
            Upload
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
