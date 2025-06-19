from typing import Dict, List


class SkillCategories:
    @staticmethod
    def get_default_skills() -> Dict[str, List[str]]:
        return {
            "frontend": [
                "react", "react.js", "reactjs", "vue.js", "vue", "vuejs", "angular", "svelte", "ember.js", "backbone.js", "preact", "alpine.js",
                "html", "css", "scss", "less", "javascript", "typescript", "xml",
                "tailwind", "bootstrap", "bulma", "material ui", "mantine", "chakra ui", "semantic", "semantic ui", "mui"
                "next.js", "nextjs", "nuxt.js", "vite", "webpack", "parcel", "rollup", "babel", "esbuild",
                "styled-components", "emotion", "redux", "zustand", "mobx", "xstate", "d3js", "d3.js", "gsap", "framer motion", "framer-motion", "razor", "blazor", "pug", "handlebars", "handlebars.js", "ejs", "twig.js", "twig", "jade", "jotai", "jquery", "lodash", "bulma", "jsx", "tsx", "pinia", "ionic", "npm", "pnpm", "hugo", "gatsby", "astro", "qwik", "solid", "solidjs"
            ],
            "backend": [
                "node.js", "nodejs", "express", "express.js", "expressjs", "fastify", "nestjs", "hapi", "koa", "sails.js", "meteor.js",
                "python", "flask", "django", "fastapi", "pyramid", "tornado", "web2py",
                "java", "spring", "spring boot", "quarkus", "micronaut", "play framework (scala/java)", "vertx", "bson"
                "php", "laravel", "symfony", "codeigniter", "zend framework", "yii", "cakephp",
                "ruby", "rails", "sinatra", "hanami",
                "go", "gin", "echo", "fiber", "beego", "revel",
                "c#", ".net", "asp.net", "asp.net core", "blazor server", "f#",
                "kotlin", "ktor",
                "rust", "rocket", "axum", "warp", "actix-web",
                "c", "c++", "cpprestsdk", "pistache",
                "grpc", "graphql", "rest", "rpc", "openapi", "json", "axios",
                "django templates", "jinja2", "twig", "blade", "erb", "haml", "slim ", "thymeleaf", "freemarker", "velocity", "pystache", "mako"],
            "database": [
                "sql", "nosql", "mysql", "mariadb", "postgresql", "sqlite", "mongodb", "cassandra", "couchbase", "couchdb",
                "neo4j", "dgraph", "arangodb", "faunadb", "dynamodb", "redis", "memcached", "timescaledb",
                "clickhouse", "influxdb", "snowflake", "bigquery", "redshift", "oracle", "sql server",
                "db2", "elasticsearch", "meilisearch", "solr",  "algolia",
                "firestore", "supabase", "firebase", "milvus", "arangodb", "orientdb", "marklogic", "azure cosmos db", "couchbase", "interSystems IRIS",       "timescaledb", "influxdb", "prometheus", "questdb", "amazon timestream", "graphite", "opentsdb", "kdb+", "victoriametrics", "tdengine", "cratedb", "sgbd", "rdbms"
            ],
            "cloud_devops": [
                "aws", "azure", "gcp", "ibm cloud", "oracle cloud", "heroku", "vercel", "netlify",
                "digitalocean", "linode", "cloudflare", "fly.io",
                "docker", "kubernetes", "helm", "istio", "linkerd", "cilium",
                "terraform", "pulumi", "cloudformation", "packer", "ansible", "saltstack", "chef",
                "jenkins", "github actions", "gitlab ci", "circleci", "argo cd", "flux", "spinnaker",
                "prometheus", "grafana", "datadog", "new relic", "sentry", "logstash", "loki", "elk stack",
                "splunk", "papertrail", "jaeger", "opentelemetry", "zabbix"
            ],
            "mobile": [
                "android", "ios", "react native", "flutter", "swift", "objective-c", "kotlin", "java",
                "xamarin", "cordova", "ionic", "unity mobile", "jetpack compose", "swiftui"
            ],
            "data_science": [
                "python", "r", "julia", "matlab", "sas", "stata", "spss", "numpy", "pandas", "dask",
                "scikit-learn", "matplotlib", "seaborn", "plotly", "bokeh", "altair",
                "tensorflow", "pytorch", "keras", "mxnet", "lightgbm", "xgboost", "catboost",
                "mlflow", "optuna", "skopt", "jupyter", "streamlit", "voila", "dash"
            ],
            "ai_ml": [
                "machine learning", "deep learning", "nlp", "computer vision", "reinforcement learning",
                "huggingface", "transformers", "openai", "llms", "chatgpt", "gpt-4", "bert", "t5", "llama",
                "embedding models", "vector databases", "pinecone", "weaviate", "milvus", "chroma", "faiss",
                "rag", "langchain", "haystack", "diffusers", "stable diffusion", "openCV", "spacy", "nltk",
                "text classification", "ner", "topic modeling", "data analysis", "data science", "data visualization"
            ],
            "testing": [
                "jest", "mocha", "chai", "vitest", "ava", "junit", "pytest", "nose", "unittest", "cypress",
                "playwright", "selenium", "robot framework", "testcafe", "postman", "karate",
                "tdd", "bdd", "unit testing", "integration testing", "load testing", "performance testing",
                "mutation testing"
            ],
            "operating_systems": [
                "linux", "windows", "macos", "unix", "ubuntu", "debian", "fedora", "centos", "arch linux", "arch",
                "redhat", "opensuse", "alpine linux", "android os", "ios", "windows server", "raspbian",
                "rtos", "tizen", "chromeos", "bsd", "freebsd", "netbsd", "openbsd",
                "bash scripting", "shell scripting", "powershell scripting", "system administration",
                "kernel development", "bootloaders", "systemd", "init", "upstart", "DOS", "solaris"
            ],
            "security": [
                "owasp", "ssl", "tls", "jwt", "oauth2", "oidc", "saml", "iam", "zero trust",
                "penetration testing", "ethical hacking", "burp suite", "wireshark", "firewalls", "siem",
                "cloud security", "devsecops", "keycloak", "auth0", "azure ad", "vault", "hashicorp",
                "threat modeling", "vulnerability scanning", "sonarqube", "snyk", "veracode",  "firewall (hardware/software)", "intrusion detection system (ids)", "intrusion prevention system (ips)",
                "vpn (virtual private network)", "network access control (nac)", "ddos", "ddos protection",
                "network segmentation", "web application firewall", "waf", "dns security", "email security gateway",
                "secure web gateway (swg)", "next-gen firewall (ngfw)", "network detection and response (ndr)",
                "snort", "wireshark", "nmap"
            ],
            "game_dev": [
                "unity", "unreal engine", "godot", "gamemaker", "construct", "defold", "c#", "blueprints",
                "openGL", "vulkan", "directx", "shaderlab", "hlsl", "glsl", "raycasting", "physics engine",
                "box2d", "physx", "spine", "aseprite", "spritekit", "tilemaps", "multiplayer networking",
                "steamworks", "glad", "glfw", "glew"
            ],
            "web3": [
                "blockchain", "ethereum", "solidity", "rust", "cadence", "substrate", "web3.js", "ethers.js",
                "truffle", "hardhat", "ganache", "polygon", "binance smart chain", "zk-rollups", "zk-snarks",
                "starknet", "smart contracts", "dapps", "ipfs", "filecoin", "arweave", "alchemy", "infura",
                "walletconnect", "metamask"
            ],
            "embedded_systems": [
                "c", "c++", "embedded c", "rtos", "freertos", "arm cortex", "esp32", "stm32", "arduino",
                "raspberry pi", "low-level programming", "device drivers", "uart", "i2c", "spi", "can bus",
                "bare-metal", "vhdl", "verilog", "fpga", "pic", "mips", "atmel", "nrf52", "real-time systems"
            ],
            "analytics_bi": [
                "power bi", "tableau", "looker", "qlik", "superset", "metabase", "datastudio", "dashboards",
                "excel", "google sheets", "kibana", "redash", "insight software", "reporting tools",
                "data storytelling", "etl", "data wrangling"
            ],
            "programming_languages": [
                "python", "javascript", "typescript", "java", "kotlin", "swift", "objective-c", "c", "cpp", "scheme",
                "c++", "c#", "visual basic", "visualbasic", "vb", "go", "rust", "ruby", "php", "scala", "r", "dart", "elixir", "haskell",
                "lua", "perl", "bash", "powershell", "assembly", "matlab", "julia", "zig", "nim",
                "vlang", "groovy", "f#", "vb.net", "coffeescript", "clojure"
            ],
            "soft_skills": [
                "communication", "teamwork", "problem solving", "adaptability", "leadership",
                "creativity", "time management", "critical thinking", "empathy", "collaboration",
                "conflict resolution", "agile mindset", "scrum", "mentoring", "decision making",
                "project management", "self-management", "ownership"
            ],
            "tools": [
                "vscode", "intellij", "eclipse", "pycharm", "webstorm", "xcode", "android studio",
                "postman", "insomnia", "figma", "zeplin", "draw.io", "notion", "obsidian",
                "jira", "confluence", "asana", "monday", "trello", "github", "gitlab", "bitbucket",
                "docker", "kubernetes", "helm", "cmake", "make", "gdb", "lldb"
            ],
            "data_engineering": [
                "kafka", "airflow", "dbt", "apache spark", "apache hadoop", "apache flink", "apache kafka", "apache nifi", "apache airflow",
                "apache beam", "apache iceberg", "apache hudi", "delta lake", "dbt (data build tool)",
                "apache zookeeper", "apache avro", "apache parquet", "apache orc", "apache arrow",
                "luigi", "prefect", "dagster", "azkaban",
                "aws glue", "aws emr", "google cloud dataflow", "google cloud dataproc", "azure data factory", "azure databricks",
                "databricks", "snowflake", "stitch", "fivetran", "matillion",
                "etl", "elt", "data warehousing", "data lakes", "data pipelines", "stream processing", "batch processing",
                "python", "nltk", "pandas", "numpy", "spacy"
            ],
            "message_queue_and_streaming": [
                "kafka", "apache kafka", "rabbitmq", "apache activemq", "amazon sqs", "amazon kinesis", "google cloud pub/sub",
                "azure service bus", "nats", "zeromq", "redis pub/sub", "mqtt", "celery (with a message broker)"
            ],
            "computer_graphics": [
                "opengl", "opengl es", "vulkan", "directx", "metal", "webgl", "webgpu",
                "three.js", "babylon.js", "p5.js", "processing", "openframeworks", "cinder",
                "unity", "unreal engine", "godot engine",
                "o3de", "diligent engine", "bgfx", "imlib", "dear imgui",
                "assimp", "glad", "glfw", "glew", "freeglut", "sokol",
                "glsl", "hlsl", "msl", "wgsl",
                "rasterization", "ray tracing", "path tracing", "global illumination",
                "physically based rendering", "deferred shading", "forward rendering",
                "ambient occlusion", "shadow mapping", "reflection mapping", "normal mapping",
                "tessellation", "subdivision surfaces", "volumetric rendering",
                "blender", "autodesk maya", "autodesk 3ds max", "cinema 4d", "zbrush",
                "substance painter", "substance designer", "marvelous designer", "houdini",
                "mixamo", "rigify", "mocap",
                "opencv", "openexr", "usd",
                "physics engines", "physx", "bullet", "virtual reality", "augmented reality",
                "mixed reality", "gpu computing", "cuda", "opencl", "voxel graphics",
                "procedural generation", "level of detail", "frustum culling", "occlusion culling"
            ]
        }

    @staticmethod
    def get_tech_skills() -> Dict[str, List[str]]:
        skills = SkillCategories.get_default_skills()
        return {k: v for k, v in skills.items() if k != "soft_skills"}

    @staticmethod
    def get_skill_to_category_mapping(skills: Dict[str, List[str]]) -> Dict[str, str]:
        """mapping from skill to category"""
        mapping = {}
        for category, skill_list in skills.items():
            for skill in skill_list:
                mapping[skill] = category
        return mapping

    @staticmethod
    def get_all_skills_flat(skills: Dict[str, List[str]]) -> List[str]:
        all_skills = []
        for skill_list in skills.values():
            all_skills.extend(skill_list)
        return all_skills

    @classmethod
    def create_custom_categories(cls, custom_skills: Dict[str, List[str]]) -> Dict[str, List[str]]:
        default_skills = cls.get_default_skills()

        # copy to avoid modifying original
        merged_skills = default_skills.copy()

        # add/append to categories
        for category, skills in custom_skills.items():
            if category in merged_skills:
                # append to an existing category
                merged_skills[category].extend(skills)
                # remove duplicates but preserve order
                merged_skills[category] = list(
                    dict.fromkeys(merged_skills[category]))
            else:
                merged_skills[category] = skills

        return merged_skills
