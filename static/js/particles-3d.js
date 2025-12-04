/**
 * 3D Particle Network Animation
 * Creates an interactive particle network background using Three.js
 */

class ParticleNetwork {
    constructor() {
        this.canvas = document.getElementById('particles-canvas');
        if (!this.canvas) {
            console.warn('Particles canvas not found');
            return;
        }

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true
        });
        
        this.particles = [];
        this.particleCount = 100;
        this.maxDistance = 150;
        this.mouse = { x: 0, y: 0 };
        
        this.init();
    }

    init() {
        // Setup renderer
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Setup camera
        this.camera.position.z = 400;
        
        // Create particles
        this.createParticles();
        
        // Create connections
        this.createConnections();
        
        // Event listeners
        window.addEventListener('resize', () => this.onWindowResize());
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
        
        // Start animation
        this.animate();
    }

    createParticles() {
        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];
        
        // Color palette
        const color1 = new THREE.Color(0x6366f1); // Primary
        const color2 = new THREE.Color(0x8b5cf6); // Secondary
        const color3 = new THREE.Color(0x06b6d4); // Accent
        
        for (let i = 0; i < this.particleCount; i++) {
            const x = Math.random() * 800 - 400;
            const y = Math.random() * 600 - 300;
            const z = Math.random() * 400 - 200;
            
            positions.push(x, y, z);
            
            // Random color from palette
            const colorChoice = Math.random();
            const color = colorChoice < 0.33 ? color1 : colorChoice < 0.66 ? color2 : color3;
            colors.push(color.r, color.g, color.b);
            
            // Store particle data for connections
            this.particles.push({
                position: new THREE.Vector3(x, y, z),
                velocity: new THREE.Vector3(
                    (Math.random() - 0.5) * 0.5,
                    (Math.random() - 0.5) * 0.5,
                    (Math.random() - 0.5) * 0.5
                )
            });
        }
        
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 3,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });
        
        this.particleSystem = new THREE.Points(geometry, material);
        this.scene.add(this.particleSystem);
    }

    createConnections() {
        this.linesMaterial = new THREE.LineBasicMaterial({
            vertexColors: true,
            transparent: true,
            opacity: 0.3
        });
        
        this.linesGroup = new THREE.Group();
        this.scene.add(this.linesGroup);
    }

    updateConnections() {
        // Remove old lines
        while (this.linesGroup.children.length > 0) {
            this.linesGroup.remove(this.linesGroup.children[0]);
        }
        
        // Create new connections
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const distance = this.particles[i].position.distanceTo(this.particles[j].position);
                
                if (distance < this.maxDistance) {
                    const geometry = new THREE.BufferGeometry();
                    const positions = new Float32Array([
                        this.particles[i].position.x,
                        this.particles[i].position.y,
                        this.particles[i].position.z,
                        this.particles[j].position.x,
                        this.particles[j].position.y,
                        this.particles[j].position.z
                    ]);
                    
                    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
                    
                    const opacity = 1 - (distance / this.maxDistance);
                    const material = this.linesMaterial.clone();
                    material.opacity = opacity * 0.3;
                    
                    const line = new THREE.Line(geometry, material);
                    this.linesGroup.add(line);
                }
            }
        }
    }

    updateParticles() {
        const positions = this.particleSystem.geometry.attributes.position.array;
        
        for (let i = 0; i < this.particles.length; i++) {
            // Update position
            this.particles[i].position.add(this.particles[i].velocity);
            
            // Boundary check
            if (Math.abs(this.particles[i].position.x) > 400) {
                this.particles[i].velocity.x *= -1;
            }
            if (Math.abs(this.particles[i].position.y) > 300) {
                this.particles[i].velocity.y *= -1;
            }
            if (Math.abs(this.particles[i].position.z) > 200) {
                this.particles[i].velocity.z *= -1;
            }
            
            // Update buffer
            positions[i * 3] = this.particles[i].position.x;
            positions[i * 3 + 1] = this.particles[i].position.y;
            positions[i * 3 + 2] = this.particles[i].position.z;
        }
        
        this.particleSystem.geometry.attributes.position.needsUpdate = true;
    }

    onMouseMove(event) {
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        
        // Subtle camera movement
        this.camera.position.x = this.mouse.x * 20;
        this.camera.position.y = this.mouse.y * 20;
        this.camera.lookAt(this.scene.position);
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Update particles
        this.updateParticles();
        
        // Update connections every few frames for performance
        if (Math.random() < 0.1) {
            this.updateConnections();
        }
        
        // Rotate scene slightly
        this.particleSystem.rotation.y += 0.0005;
        
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Check if Three.js is loaded
    if (typeof THREE !== 'undefined') {
        new ParticleNetwork();
    } else {
        console.warn('Three.js not loaded, skipping particle animation');
    }
});
