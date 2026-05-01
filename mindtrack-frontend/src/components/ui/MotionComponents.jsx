import { motion } from "framer-motion";
import { cn } from "../../utils/cn";

// Card yang ikut bergerak saat kursor mendekat
export function HoverCard({ children, className }) {
  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}

// Teks yang muncul dengan efek blur-in dari bawah
export function BlurFadeText({ children, className, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
      whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.7, delay, ease: "easeOut" }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}

// Section yang muncul dengan slide-up
export function FadeInSection({ children, className, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6, delay, ease: "easeOut" }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}

// Number counter animation
export function CountUp({ from = 0, to, suffix = "", className }) {
  return (
    <motion.span
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      className={cn(className)}
    >
      <motion.span
        initial={{ innerText: from }}
        whileInView={{ innerText: to }}
        viewport={{ once: true }}
        transition={{ duration: 2, ease: "easeOut" }}
        onUpdate={(latest) => {}}
      >
        {to}{suffix}
      </motion.span>
    </motion.span>
  );
}

// Parallax wrapper dengan useScroll
export function ParallaxSection({ children, className }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}
