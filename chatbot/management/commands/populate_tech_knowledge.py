from django.core.management.base import BaseCommand
from chatbot.models import KnowledgeBase
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the knowledge base with tech and programming Q&A entries'

    def handle(self, *args, **kwargs):
        tech_entries = [
            {
                'question': 'What is Python?',
                'answer': 'Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python is widely used in web development, data science, artificial intelligence, automation, and more.'
            },
            {
                'question': 'What is Django?',
                'answer': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the Model-View-Template (MVT) architectural pattern and includes features like an ORM, authentication system, admin interface, and built-in security measures.'
            },
            {
                'question': 'What is the difference between Python 2 and Python 3?',
                'answer': 'Python 3 is the current version with improved Unicode support, better syntax, and enhanced features. Key differences include: print is a function in Python 3, integer division returns float, improved exception handling, and better Unicode string handling. Python 2 reached end-of-life in 2020.'
            },
            {
                'question': 'What is a database?',
                'answer': 'A database is an organized collection of structured data stored electronically. It allows for efficient storage, retrieval, and management of information. Common types include relational databases (MySQL, PostgreSQL), NoSQL databases (MongoDB, Redis), and cloud databases.'
            },
            {
                'question': 'What is MySQL?',
                'answer': 'MySQL is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL). It is widely used for web applications and is known for its reliability, performance, and ease of use. MySQL is part of the LAMP stack (Linux, Apache, MySQL, PHP/Python/Perl).'
            },
            {
                'question': 'What is an API?',
                'answer': 'API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other. APIs define the methods and data formats that applications can use to request and exchange information. REST and GraphQL are popular API architectures.'
            },
            {
                'question': 'What is Git?',
                'answer': 'Git is a distributed version control system used to track changes in source code during software development. It allows multiple developers to work on the same project simultaneously, maintains a complete history of changes, and enables branching and merging of code.'
            },
            {
                'question': 'What is the difference between frontend and backend?',
                'answer': 'Frontend refers to the client-side of an application - what users see and interact with (HTML, CSS, JavaScript). Backend refers to the server-side - databases, server logic, and APIs that power the application. Full-stack developers work on both frontend and backend.'
            },
            {
                'question': 'What is object-oriented programming?',
                'answer': 'Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects, which contain data (attributes) and code (methods). Key principles include encapsulation, inheritance, polymorphism, and abstraction. Languages like Python, Java, and C++ support OOP.'
            },
            {
                'question': 'What is a virtual environment in Python?',
                'answer': 'A virtual environment is an isolated Python environment that allows you to install packages and dependencies specific to a project without affecting the global Python installation. Tools like venv, virtualenv, and conda are used to create virtual environments.'
            },
            {
                'question': 'What is HTML?',
                'answer': 'HTML (HyperText Markup Language) is the standard markup language for creating web pages. It uses tags to structure content, define headings, paragraphs, links, images, and other elements. HTML5 is the latest version with enhanced multimedia and semantic features.'
            },
            {
                'question': 'What is CSS?',
                'answer': 'CSS (Cascading Style Sheets) is a stylesheet language used to describe the presentation and styling of HTML documents. It controls layout, colors, fonts, spacing, and responsive design. Modern CSS includes features like Flexbox, Grid, and animations.'
            },
            {
                'question': 'What is JavaScript?',
                'answer': 'JavaScript is a high-level, interpreted programming language primarily used for creating interactive web pages. It runs in web browsers and enables dynamic content, form validation, animations, and asynchronous operations. Node.js allows JavaScript to run on servers as well.'
            },
            {
                'question': 'What is machine learning?',
                'answer': 'Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions. Common types include supervised, unsupervised, and reinforcement learning.'
            },
            {
                'question': 'What is cloud computing?',
                'answer': 'Cloud computing is the delivery of computing services (servers, storage, databases, networking, software) over the internet. Major providers include AWS, Google Cloud, and Microsoft Azure. Benefits include scalability, cost-efficiency, and accessibility from anywhere.'
            },
            {
                'question': 'What is REST API?',
                'answer': 'REST (Representational State Transfer) is an architectural style for designing networked applications. REST APIs use HTTP methods (GET, POST, PUT, DELETE) to perform CRUD operations. They are stateless, cacheable, and use standard HTTP status codes for responses.'
            },
            {
                'question': 'What is SQL?',
                'answer': 'SQL (Structured Query Language) is a standard language for managing and manipulating relational databases. It includes commands for querying data (SELECT), inserting (INSERT), updating (UPDATE), deleting (DELETE), and defining database structures (CREATE, ALTER, DROP).'
            },
            {
                'question': 'What is debugging?',
                'answer': 'Debugging is the process of finding and fixing errors or bugs in software code. Techniques include using debuggers, print statements, logging, breakpoints, and step-through execution. Good debugging skills are essential for software development.'
            },
            {
                'question': 'What is responsive design?',
                'answer': 'Responsive web design is an approach that makes web pages render well on various devices and screen sizes. It uses flexible layouts, media queries, and fluid grids to adapt content. This ensures optimal viewing experience on desktops, tablets, and mobile devices.'
            },
            {
                'question': 'What is a framework?',
                'answer': 'A framework is a pre-built structure that provides a foundation for developing applications. It includes libraries, tools, and best practices that speed up development. Examples include Django and Flask for Python, React and Angular for JavaScript, and Spring for Java.'
            },
            {
                'question': 'What is version control?',
                'answer': 'Version control is a system that tracks changes to files over time. It allows developers to collaborate, revert to previous versions, and maintain a history of modifications. Git is the most popular version control system, often used with platforms like GitHub, GitLab, or Bitbucket.'
            },
            {
                'question': 'What is agile methodology?',
                'answer': 'Agile is a software development methodology that emphasizes iterative development, collaboration, and flexibility. It involves breaking projects into small increments (sprints), continuous feedback, and adapting to changing requirements. Scrum and Kanban are popular agile frameworks.'
            },
            {
                'question': 'What is data science?',
                'answer': 'Data science is an interdisciplinary field that uses scientific methods, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines statistics, machine learning, data analysis, and domain expertise to solve complex problems.'
            },
            {
                'question': 'What is cybersecurity?',
                'answer': 'Cybersecurity is the practice of protecting systems, networks, and data from digital attacks, unauthorized access, and damage. It includes measures like encryption, firewalls, authentication, intrusion detection, and security best practices to safeguard information.'
            },
            {
                'question': 'What is DevOps?',
                'answer': 'DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and deliver high-quality software continuously. It emphasizes automation, collaboration, continuous integration/deployment (CI/CD), and monitoring.'
            },
            {
                'question': 'What is the difference between compiler and interpreter?',
                'answer': 'A compiler translates entire source code into machine code before execution (e.g., C, C++), resulting in faster execution but longer compilation time. An interpreter executes code line-by-line at runtime (e.g., Python, JavaScript), allowing for easier debugging but slower execution.'
            },
            {
                'question': 'What is Docker?',
                'answer': 'Docker is a platform that uses containerization to package applications and their dependencies into standardized units called containers. Containers are lightweight, portable, and ensure consistent behavior across different environments, making deployment and scaling easier.'
            },
            {
                'question': 'What is a data structure?',
                'answer': 'A data structure is a way of organizing and storing data to enable efficient access and modification. Common data structures include arrays, linked lists, stacks, queues, trees, graphs, hash tables, and heaps. Choosing the right data structure is crucial for algorithm efficiency.'
            },
            {
                'question': 'What is an algorithm?',
                'answer': 'An algorithm is a step-by-step procedure or set of rules for solving a problem or performing a task. Algorithms are fundamental to computer science and programming. They are evaluated based on time complexity, space complexity, and correctness.'
            },
            {
                'question': 'What is Bootstrap?',
                'answer': 'Bootstrap is a popular open-source CSS framework for building responsive, mobile-first websites. It provides pre-designed components, grid system, utilities, and JavaScript plugins that speed up frontend development and ensure consistent design across browsers.'
            },
        ]

        created_count = 0
        skipped_count = 0

        for entry in tech_entries:
            # Check if question already exists
            if not KnowledgeBase.objects.filter(question=entry['question']).exists():
                KnowledgeBase.objects.create(
                    question=entry['question'],
                    answer=entry['answer']
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Added: {entry["question"][:60]}...'))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'⊘ Skipped (already exists): {entry["question"][:60]}...'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} tech/programming knowledge base entries'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped {skipped_count} existing entries'))
