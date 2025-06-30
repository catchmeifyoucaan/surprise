import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Eye, 
  EyeOff, 
  Mail, 
  Lock, 
  Github, 
  MessageSquare, 
  Send, 
  Plus, 
  Code, 
  Play, 
  Settings, 
  User,
  LogOut,
  FolderPlus,
  Trash2,
  Copy,
  Download,
  ExternalLink,
  Sparkles,
  Zap,
  Brain,
  Terminal,
  FileCode,
  Layers,
  Globe
} from 'lucide-react';

// Login Page Component
export const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    onLogin();
    setIsLoading(false);
  };

  const handleOAuthLogin = (provider) => {
    // Mock OAuth login
    onLogin();
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 opacity-90"></div>
      
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-blue-500 rounded-full opacity-20"
            initial={{ 
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
              scale: 0 
            }}
            animate={{ 
              scale: [0, 1, 0],
              opacity: [0, 0.3, 0]
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 w-full max-w-md space-y-8"
      >
        {/* Logo and Header */}
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="mx-auto w-16 h-16 bg-white rounded-full flex items-center justify-center mb-6"
          >
            <div className="text-2xl font-bold text-gray-900">E</div>
          </motion.div>
          <h1 className="text-3xl font-bold text-white mb-2">Welcome to Emergent</h1>
          <p className="text-gray-400">
            Don't have an account? 
            <span className="text-blue-400 cursor-pointer hover:text-blue-300 ml-1">
              Sign up for free
            </span>
          </p>
        </div>

        {/* OAuth Buttons */}
        <div className="space-y-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => handleOAuthLogin('google')}
            className="w-full flex items-center justify-center px-4 py-3 border border-gray-600 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors"
          >
            <div className="w-5 h-5 mr-3 bg-white rounded-full flex items-center justify-center">
              <span className="text-xs font-bold text-gray-900">G</span>
            </div>
            Log in with Google
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => handleOAuthLogin('github')}
            className="w-full flex items-center justify-center px-4 py-3 border border-gray-600 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-colors"
          >
            <Github className="w-5 h-5 mr-3" />
            Log in with GitHub
          </motion.button>
        </div>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-600"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-gray-900 text-gray-400">Or Log in with email</span>
          </div>
        </div>

        {/* Email/Password Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="w-full pl-10 pr-12 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-white text-gray-900 rounded-lg font-medium hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-gray-900 border-t-transparent rounded-full animate-spin mr-2"></div>
                Logging in...
              </div>
            ) : (
              'Log In'
            )}
          </motion.button>
        </form>

        {/* Forgot Password */}
        <div className="text-center">
          <a href="#" className="text-blue-400 hover:text-blue-300 text-sm">
            Forgot Password?
          </a>
        </div>

        {/* Footer */}
        <div className="absolute bottom-4 left-0 right-0 text-center text-gray-500 text-sm">
          <div className="flex items-center justify-center space-x-4">
            <span>emergent</span>
            <span>•</span>
            <span>2025</span>
          </div>
          <div className="flex items-center justify-center space-x-4 mt-2">
            <a href="#" className="hover:text-gray-300">Privacy Policy</a>
            <span>•</span>
            <a href="#" className="hover:text-gray-300">Terms of Service</a>
            <span>•</span>
            <a href="#" className="hover:text-gray-300">Copyright</a>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

// Chat Message Component
export const ChatMessage = ({ message, isUser, timestamp, code, language }) => {
  const [showExecuteButton, setShowExecuteButton] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);

  useEffect(() => {
    setShowExecuteButton(!!code && !isUser);
  }, [code, isUser]);

  const executeCode = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          language: language || 'python',
          user_id: 'demo-user'
        })
      });

      const result = await response.json();
      setExecutionResult(result);
    } catch (error) {
      setExecutionResult({
        success: false,
        error: error.message
      });
    }
  };

  // Function to render markdown-style message
  const renderMessage = (text) => {
    // Convert **text** to bold
    let rendered = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert ```code``` blocks to styled code
    rendered = rendered.replace(/```(\w+)?\n?([\s\S]*?)```/g, (match, lang, code) => {
      return `<div class="code-block">
        <div class="code-header">${lang || 'code'}</div>
        <pre><code>${code.trim()}</code></pre>
      </div>`;
    });
    
    // Convert `inline code` to styled inline code
    rendered = rendered.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Convert line breaks
    rendered = rendered.replace(/\n/g, '<br>');
    
    return rendered;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`max-w-[80%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? 'bg-blue-500' : 'bg-gray-700'
          }`}>
            {isUser ? (
              <User className="w-4 h-4 text-white" />
            ) : (
              <Brain className="w-4 h-4 text-white" />
            )}
          </div>
          <div className={`rounded-lg px-4 py-2 ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-800 text-gray-200 border border-gray-700'
          }`}>
            <div 
              className="text-sm message-content"
              dangerouslySetInnerHTML={{ __html: renderMessage(message) }}
            />
            <div className="flex items-center justify-between mt-2">
              <p className="text-xs opacity-70">{timestamp}</p>
              {showExecuteButton && (
                <button
                  onClick={executeCode}
                  className="ml-2 px-2 py-1 bg-green-500 hover:bg-green-600 text-white text-xs rounded transition-colors"
                >
                  <Play className="w-3 h-3 inline mr-1" />
                  Run Code
                </button>
              )}
            </div>
            
            {/* Execution Result */}
            {executionResult && (
              <div className="mt-3 p-3 bg-gray-900 rounded border">
                <div className="flex items-center space-x-2 mb-2">
                  <Terminal className="w-4 h-4" />
                  <span className="text-xs font-medium">Execution Result:</span>
                </div>
                {executionResult.success ? (
                  <pre className="text-green-400 text-xs whitespace-pre-wrap">
                    {executionResult.output || 'Code executed successfully (no output)'}
                  </pre>
                ) : (
                  <pre className="text-red-400 text-xs whitespace-pre-wrap">
                    Error: {executionResult.error}
                  </pre>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Project Card Component
export const ProjectCard = ({ project, onSelect, onDelete }) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onSelect(project)}
      className="bg-gray-800 border border-gray-700 rounded-lg p-4 cursor-pointer hover:border-blue-500 transition-colors"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
            <Code className="w-4 h-4 text-white" />
          </div>
          <div>
            <h3 className="text-white font-medium">{project.name}</h3>
            <p className="text-gray-400 text-sm">{project.type}</p>
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(project.id);
          }}
          className="text-gray-400 hover:text-red-400 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
      <p className="text-gray-400 text-sm mb-3">{project.description}</p>
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-500">{project.lastModified}</span>
        <div className="flex items-center space-x-2">
          <span className={`w-2 h-2 rounded-full ${
            project.status === 'deployed' ? 'bg-green-500' : 
            project.status === 'building' ? 'bg-yellow-500' : 'bg-gray-500'
          }`}></span>
          <span className="text-xs text-gray-400 capitalize">{project.status}</span>
        </div>
      </div>
    </motion.div>
  );
};

// Code Editor Component
export const CodeEditor = ({ code, language, onChange }) => {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <FileCode className="w-4 h-4 text-gray-400" />
          <span className="text-sm text-gray-400">{language}</span>
        </div>
        <div className="flex items-center space-x-2">
          <button className="text-gray-400 hover:text-white">
            <Copy className="w-4 h-4" />
          </button>
          <button className="text-gray-400 hover:text-white">
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-96 p-4 bg-gray-900 text-gray-200 font-mono text-sm resize-none focus:outline-none"
        placeholder="Your code will appear here..."
      />
    </div>
  );
};

// Sidebar Component
export const Sidebar = ({ activeTab, setActiveTab, projects, onNewProject, onLogout }) => {
  const tabs = [
    { id: 'chat', label: 'AI Assistant', icon: MessageSquare },
    { id: 'projects', label: 'Projects', icon: FolderPlus },
    { id: 'code', label: 'Code Editor', icon: Code },
    { id: 'deploy', label: 'Deploy', icon: ExternalLink },
  ];

  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
            <div className="text-lg font-bold text-gray-900">E</div>
          </div>
          <span className="text-white font-medium">Emergent</span>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                activeTab === tab.id
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-sm">{tab.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-gray-700">
        <button
          onClick={onNewProject}
          className="w-full flex items-center space-x-2 px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors mb-3"
        >
          <Plus className="w-4 h-4" />
          <span className="text-sm">New Project</span>
        </button>
        
        <button
          onClick={onLogout}
          className="w-full flex items-center space-x-2 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm">Logout</span>
        </button>
      </div>
    </div>
  );
};

// Main Dashboard Component
export const Dashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('chat');
  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'E-commerce Platform',
      type: 'React + Node.js',
      description: 'Full-stack e-commerce platform with payment integration',
      lastModified: '2 hours ago',
      status: 'deployed'
    },
    {
      id: 2,
      name: 'Task Manager App',
      type: 'React + FastAPI',
      description: 'Collaborative task management application',
      lastModified: '1 day ago',
      status: 'building'
    },
    {
      id: 3,
      name: 'Weather Dashboard',
      type: 'Vue.js + Express',
      description: 'Real-time weather monitoring dashboard',
      lastModified: '3 days ago',
      status: 'draft'
    }
  ]);

  const [messages, setMessages] = useState([
    {
      id: 1,
      message: "Hello! I'm your AI coding assistant. I can help you build applications, write code, and deploy your projects. What would you like to create today?",
      isUser: false,
      timestamp: new Date().toLocaleTimeString()
    }
  ]);

  const [inputMessage, setInputMessage] = useState('');
  const [code, setCode] = useState('// Welcome to Emergent Code Editor\n// Start typing your code here...\n\nfunction hello() {\n  console.log("Hello, World!");\n}');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      message: inputMessage,
      isUser: true,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage('');

    // Show typing indicator
    const typingMessage = {
      id: messages.length + 2,
      message: "🤖 AI is generating code...",
      isUser: false,
      timestamp: new Date().toLocaleTimeString(),
      isTyping: true
    };
    setMessages(prev => [...prev, typingMessage]);

    try {
      // Send to real AI backend
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentMessage,
          user_id: 'demo-user',
          language: 'python',
          model: 'auto'
        })
      });

      const data = await response.json();
      
      // Remove typing indicator and add real response
      setMessages(prev => {
        const withoutTyping = prev.filter(msg => !msg.isTyping);
        
        if (data.success && data.response.success) {
          const aiMessage = {
            id: withoutTyping.length + 1,
            message: `✨ **Code Generated Successfully!**\n\n**Model Used:** ${data.response.model_used}\n\n**Code:**\n\`\`\`${data.response.language}\n${data.response.code}\n\`\`\`\n\n**Explanation:** ${data.response.explanation}`,
            isUser: false,
            timestamp: new Date().toLocaleTimeString(),
            code: data.response.code,
            language: data.response.language
          };
          return [...withoutTyping, aiMessage];
        } else {
          const errorMessage = {
            id: withoutTyping.length + 1,
            message: `❌ Error: ${data.response?.error || 'Failed to generate code'}\n\nTip: Make sure AI API keys are configured in backend/.env`,
            isUser: false,
            timestamp: new Date().toLocaleTimeString()
          };
          return [...withoutTyping, errorMessage];
        }
      });

    } catch (error) {
      // Remove typing indicator and show error
      setMessages(prev => {
        const withoutTyping = prev.filter(msg => !msg.isTyping);
        const errorMessage = {
          id: withoutTyping.length + 1,
          message: `❌ Connection Error: ${error.message}\n\nPlease check if the backend is running.`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString()
        };
        return [...withoutTyping, errorMessage];
      });
    }
  };

  const handleNewProject = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: 'New AI-generated project',
          tech_stack: 'React + FastAPI',
          user_id: 'demo-user'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const newProject = {
          id: data.project_id,
          name: data.project_name,
          type: 'React + FastAPI',
          description: 'A new project created with AI assistance',
          lastModified: 'Just now',
          status: 'created'
        };
        setProjects(prev => [newProject, ...prev]);
        setActiveTab('projects');
        
        // Show success message
        const successMessage = {
          id: messages.length + 1,
          message: `🎉 Project "${data.project_name}" created successfully!\n\nFiles created: ${data.files_created}\nProject ID: ${data.project_id}`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, successMessage]);
      } else {
        console.error('Failed to create project:', data.error);
      }
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  const handleDeleteProject = (projectId) => {
    setProjects(prev => prev.filter(p => p.id !== projectId));
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return (
          <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              <div className="text-center mb-8">
                <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full">
                  <Sparkles className="w-4 h-4 text-blue-400" />
                  <span className="text-blue-400 text-sm">AI Assistant Active</span>
                </div>
              </div>
              
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message.message}
                  isUser={message.isUser}
                  timestamp={message.timestamp}
                  code={message.code}
                  language={message.language}
                />
              ))}
              <div ref={messagesEndRef} />
            </div>
            
            <div className="border-t border-gray-700 p-4">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Describe the application you want to build..."
                  className="flex-1 px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={handleSendMessage}
                  className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        );

      case 'projects':
        return (
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Your Projects</h2>
              <button
                onClick={handleNewProject}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>New Project</span>
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <ProjectCard
                  key={project.id}
                  project={project}
                  onSelect={() => setActiveTab('code')}
                  onDelete={handleDeleteProject}
                />
              ))}
            </div>
          </div>
        );

      case 'code':
        return (
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Code Editor</h2>
              <div className="flex items-center space-x-2">
                <button className="flex items-center space-x-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors">
                  <Play className="w-4 h-4" />
                  <span>Run</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
                  <Download className="w-4 h-4" />
                  <span>Download</span>
                </button>
              </div>
            </div>
            
            <CodeEditor
              code={code}
              language="javascript"
              onChange={setCode}
            />
          </div>
        );

      case 'deploy':
        return (
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Deploy & Share</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                    <Globe className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-white font-medium">Production Deployment</h3>
                    <p className="text-gray-400 text-sm">Deploy to cloud with custom domain</p>
                  </div>
                </div>
                <button className="w-full py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors">
                  Deploy Now
                </button>
              </div>
              
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                    <Zap className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-white font-medium">Preview Deployment</h3>
                    <p className="text-gray-400 text-sm">Test your app before going live</p>
                  </div>
                </div>
                <button className="w-full py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
                  Create Preview
                </button>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="h-screen bg-gray-900 flex">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        projects={projects}
        onNewProject={handleNewProject}
        onLogout={onLogout}
      />
      <div className="flex-1 overflow-hidden">
        {renderContent()}
      </div>
    </div>
  );
};