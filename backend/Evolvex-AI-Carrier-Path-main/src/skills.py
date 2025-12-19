import re

COMMON_SKILLS = [
    # Programming Languages
    'python', 'java', 'c++', 'c#', 'go', 'rust', 'typescript', 'javascript', 'swift', 'kotlin', 'ruby', 'php', 'perl', 'objective-c', 'r', 'matlab', 'dart', 'scala', 'groovy', 'lua', 'visual basic', 'assembly', 'fortran', 'cobol', 'delphi', 'abap', 'sas', 'c',
    # Web & Frameworks (Frontend & Backend, old & new)
    'html', 'html5', 'css', 'css3', 'react', 'reactjs', 'react native', 'angular', 'angularjs', 'vue', 'vuejs', 'svelte', 'ember', 'backbone', 'jquery', 'jQuery', 'bootstrap', 'tailwind', 'material-ui', 'redux', 'webpack', 'babel', 'next.js', 'nextjs', 'nuxt.js', 'nuxtjs', 'meteor', 'express', 'expressjs', 'node', 'nodejs', 'node.js', 'fastapi', 'flask', 'django', 'spring', 'spring boot', 'springboot', 'struts', 'grails', 'laravel', 'symfony', 'cakephp', 'zend', 'codeigniter', 'yii', 'asp.net', 'dotnet', '.net', 'dotnet core', '.net core', 'rails', 'ruby on rails', 'phoenix', 'play', 'fiber', 'hapi', 'koa', 'adonis', 'nestjs', 'quasar', 'alpinejs', 'stimulus', 'pyramid', 'tornado', 'bottle', 'web2py', 'cherrypy', 'coldfusion', 'servlet', 'jsp', 'blade', 'sinatra', 'mason', 'mojolicious', 'plack', 'rocket', 'actix', 'vapor', 'actix-web',
    # Full Stack/Backend/Frontend
    'full stack', 'fullstack', 'frontend', 'front-end', 'backend', 'back-end', 'rest', 'restful', 'rest api', 'graphql', 'grpc', 'microservices', 'api', 'apis', 'mvc', 'spa', 'ssr', 'pwa',
    # Data & ML
    'pandas', 'numpy', 'scipy', 'scikit-learn', 'sklearn', 'tensorflow', 'tf', 'pytorch', 'torch', 'keras', 'xgboost', 'catboost', 'lightgbm', 'mlops', 'machine learning', 'ml', 'deep learning', 'dl', 'nlp', 'natural language processing', 'computer vision', 'cv', 'data analysis', 'data science', 'data engineering', 'big data', 'analytics', 'artificial intelligence', 'ai',
    # Databases
    'sql', 'mysql', 'postgresql', 'postgres', 'mssql', 'sql server', 'sqlite', 'oracle', 'mongodb', 'mongo', 'redis', 'cassandra', 'dynamodb', 'couchdb', 'elasticsearch', 'elastic', 'neo4j', 'arangodb', 'bigquery', 'snowflake', 'databricks', 'hadoop', 'spark', 'apache spark', 'hive', 'redshift', 'clickhouse', 'influxdb', 'memcached', 'firestore', 'firebase', 'realm', 'supabase',
    # Cloud & DevOps
    'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 'google cloud', 'cloud', 'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'ci/cd', 'cicd', 'jenkins', 'airflow', 'bash', 'shell', 'bash/shell', 'powershell', 'vagrant', 'openshift', 'cloudformation', 'circleci', 'travis', 'travis ci', 'github actions', 'gitlab ci', 'argo', 'helm', 'prometheus', 'grafana', 'datadog', 'new relic', 'splunk', 'puppet', 'chef', 'saltstack', 'consul', 'nomad', 'vercel', 'netlify', 'heroku',
    # Tools & Libraries
    'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'notion', 'slack', 'excel', 'powerbi', 'power bi', 'tableau', 'looker', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'd3.js', 'd3', 'highcharts', 'chart.js', 'sqlalchemy', 'orm', 'pypdf2', 'docx', 'openpyxl', 'xlrd', 'xlwt', 'beautifulsoup', 'bs4', 'scrapy', 'requests', 'httpx', 'aiohttp', 'pytest', 'unittest', 'mocha', 'jest', 'junit', 'testing', 'selenium', 'cypress', 'playwright', 'puppeteer', 'postman', 'swagger', 'openapi', 'soapui', 'vs code', 'vscode', 'visual studio', 'intellij', 'pycharm', 'eclipse', 'vim', 'emacs',
    # LLM & AI
    'prompt engineering', 'langchain', 'openai', 'chatgpt', 'gpt', 'llm', 'llms', 'large language model', 'huggingface', 'hugging face', 'transformers', 'bert', 'gpt-3', 'gpt-4', 'llama', 'gemini', 'claude', 'anthropic', 'rag', 'vector database', 'pinecone', 'weaviate', 'chromadb',
    # Mobile
    'android', 'ios', 'flutter', 'react native', 'xamarin', 'ionic', 'cordova', 'mobile development', 'mobile app',
    # Other
    'agile', 'scrum', 'kanban', 'linux', 'unix', 'windows', 'macos', 'waterfall', 'etl', 'project management', 'leadership', 'communication', 'problem solving', 'testing', 'unit testing', 'integration testing', 'tdd', 'bdd', 'oop', 'object oriented', 'functional programming', 'soa', 'design patterns', 'system design', 'architecture', 'software architecture', 'ux', 'ui', 'ux/ui', 'ui/ux', 'user experience', 'user interface', 'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'a11y', 'accessibility', 'i18n', 'l10n', 'security', 'cybersecurity', 'networking', 'tcp/ip', 'http', 'https', 'ssl', 'tls', 'oauth', 'jwt', 'authentication', 'authorization',
]

def normalize_skill(skill):
    """Normalize skill name for matching"""
    return re.sub(r'[^a-z0-9+#]', '', skill.lower())

def extract_skills(text, skills=None):
    """
    Extract skills from text using improved matching algorithm
    
    Args:
        text: Resume or document text
        skills: Optional custom skills list
    
    Returns:
        Sorted list of unique skills found
    """
    if skills is None:
        skills = COMMON_SKILLS
    
    found = set()
    text_lower = text.lower()
    
    # Method 1: Word boundary matching (more accurate)
    for skill in skills:
        # Create regex pattern with word boundaries
        # Handle special characters in skill names
        escaped_skill = re.escape(skill.lower())
        pattern = r'\b' + escaped_skill + r'\b'
        
        if re.search(pattern, text_lower):
            # Add the properly capitalized version
            found.add(skill.title() if skill.islower() else skill)
    
    # Method 2: Normalized matching for skills that might have variations
    text_normalized = re.sub(r'[^a-z0-9+#\s]', ' ', text_lower)
    words = set(text_normalized.split())
    
    for skill in skills:
        skill_norm = normalize_skill(skill)
        # Check if normalized skill appears as a word
        if skill_norm in words:
            found.add(skill.title() if skill.islower() else skill)
        # Check for compound skills (e.g., "machine learning")
        elif ' ' not in skill and len(skill_norm) >= 2:
            if skill_norm in text_normalized.replace(' ', ''):
                found.add(skill.title() if skill.islower() else skill)
    
    # Clean up duplicates with different capitalizations
    cleaned = {}
    for skill in found:
        key = skill.lower()
        if key not in cleaned or len(skill) > len(cleaned[key]):
            cleaned[key] = skill
    
    return sorted(cleaned.values(), key=str.lower)


def get_skill_categories():
    """Return skills organized by category"""
    return {
        "Programming Languages": ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'R', 'Scala', 'Dart'],
        "Web Frameworks": ['React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Node.js', 'Express', 'Spring Boot', 'Laravel', 'Next.js', 'NestJS'],
        "Data & ML": ['Pandas', 'NumPy', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision'],
        "Databases": ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Firebase', 'DynamoDB'],
        "Cloud & DevOps": ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'CI/CD', 'GitHub Actions'],
        "Tools": ['Git', 'GitHub', 'Jira', 'VS Code', 'Postman', 'Swagger'],
        "AI & LLM": ['OpenAI', 'LangChain', 'Hugging Face', 'GPT', 'LLM', 'Prompt Engineering', 'RAG'],
    }
