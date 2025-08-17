import { useState, useEffect } from "react";
import { Cpu } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Model {
  id: string;
  name: string;
  provider: string;
  provider_icon: string;
  category: string;
  context_length: number;
  description: string;
}

interface ModelSelectorProps {
  value: string;
  onValueChange: (value: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  value,
  onValueChange,
}) => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://localhost:8123/api/models");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setModels(data.models);
        
        // Set default model if none is selected
        if (!value && data.default_model) {
          onValueChange(data.default_model);
        }
      } catch (err) {
        console.error("Failed to fetch models:", err);
        setError(err instanceof Error ? err.message : "Failed to fetch models");
        
        // // Fallback to hardcoded models if API fails
        // const fallbackModels: Model[] = [
        //   {
        //     id: "gpt-oss-20b",
        //     name: "gpt-oss-20b",
        //     provider: "OpenRouter",
        //     provider_icon: "🔗",
        //     category: "Free",
        //     context_length: 8192,
        //     description: "Free OpenAI model via OpenRouter"
        //   },
        //   {
        //     id: "gemini-2.0-flash",
        //     name: "2.0 Flash",
        //     provider: "Google",
        //     provider_icon: "⚡",
        //     category: "Paid",
        //     context_length: 8192,
        //     description: "Fast and efficient Gemini model"
        //   },
        //   {
        //     id: "gemini-2.5-flash-preview-04-17",
        //     name: "2.5 Flash",
        //     provider: "Google",
        //     provider_icon: "⚡",
        //     category: "Paid",
        //     context_length: 8192,
        //     description: "Latest Gemini Flash model"
        //   },
        //   {
        //     id: "gemini-2.5-pro-preview-05-06",
        //     name: "2.5 Pro",
        //     provider: "Google",
        //     provider_icon: "⚙️",
        //     category: "Paid",
        //     context_length: 8192,
        //     description: "High-quality Gemini Pro model"
        //   }
        // ];
        // setModels(fallbackModels);
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, [value, onValueChange]);

  const getModelDisplayName = (model: Model) => {
    if (model.provider === "OpenRouter") {
      return model.name;
    }
    return model.name;
  };

  const getModelIcon = (model: Model) => {
    if (model.provider === "OpenRouter") {
      return "🔗";
    }
    return model.provider_icon;
  };

  const getModelColor = (model: Model) => {
    if (model.provider === "OpenRouter") {
      return "text-green-400";
    }
    if (model.name.includes("Flash")) {
      return "text-yellow-400";
    }
    return "text-purple-400";
  };

  if (loading) {
    return (
      <div className="flex flex-row gap-2 bg-neutral-700 border-neutral-600 text-neutral-300 focus:ring-neutral-500 rounded-xl rounded-t-sm pl-2 max-w-[100%] sm:max-w-[90%]">
        <div className="flex flex-row items-center text-sm ml-2">
          <Cpu className="h-4 w-4 mr-2" />
          Model
        </div>
        <div className="w-[150px] bg-transparent border-none cursor-pointer text-neutral-500">
          Loading...
        </div>
      </div>
    );
  }

  if (error) {
    console.warn("Model loading error:", error);
  }

  return (
    <div className="flex flex-row gap-2 bg-neutral-700 border-neutral-600 text-neutral-300 focus:ring-neutral-500 rounded-xl rounded-t-sm pl-2 max-w-[100%] sm:max-w-[90%]">
      <div className="flex flex-row items-center text-sm ml-2">
        <Cpu className="h-4 w-4 mr-2" />
        Model
      </div>
      <Select value={value} onValueChange={onValueChange}>
        <SelectTrigger className="w-[150px] bg-transparent border-none cursor-pointer">
          <SelectValue placeholder="Model" />
        </SelectTrigger>
        <SelectContent className="bg-neutral-700 border-neutral-600 text-neutral-300 cursor-pointer max-h-[300px]">
          {models.map((model) => (
            <SelectItem
              key={model.id}
              value={model.id}
              className="hover:bg-neutral-600 focus:bg-neutral-600 cursor-pointer"
            >
              <div className="flex items-center justify-between w-full">
                <div className="flex items-center">
                  <span className={`mr-2 ${getModelColor(model)}`}>
                    {getModelIcon(model)}
                  </span>
                  <span className="mr-2">{getModelDisplayName(model)}</span>
                </div>
                <div className="flex items-center gap-2 text-xs text-neutral-400">
                  <span className={`px-2 py-1 rounded ${
                    model.category === "Free" 
                      ? "bg-green-500/20 text-green-400" 
                      : "bg-blue-500/20 text-blue-400"
                  }`}>
                    {model.category}
                  </span>
                  <span className="text-neutral-500">
                    {model.provider}
                  </span>
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};
