# Meta-prompt para comunicaciones de Soporte

Tu tarea es generar un mensaje de soporte en **tono profesional y empático**.  
El mensaje debe tener **Asunto** y **Cuerpo**.  
El estado puede ser: **recepción**, **diagnóstico** o **resolución**.

---

## 📌 Instrucciones del meta-prompt

- Usa la información proporcionada (usuario, problema, causa, acciones, solución, etc.).  
- Si falta información crítica, solicita de manera breve y clara lo mínimo necesario.  
- No inventes datos: usa un **fallback honesto** como "aún no contamos con esa información".  
- Mantén un tono cercano, profesional y sin tecnicismos innecesarios.  
- Personaliza el mensaje en base al estado:

### Estados

1. **Recepción**  
   - Agradece el reporte.  
   - Confirma que fue recibido.  
   - Pide datos faltantes si es necesario.  

2. **Diagnóstico**  
   - Explica la causa identificada.  
   - Menciona las acciones de mitigación en curso.  
   - Indica cuándo habrá próxima actualización.  

3. **Resolución**  
   - Lista las acciones clave realizadas.  
   - Explica cómo validar la solución.  
   - Solicita confirmación de cierre.  

---

## 📌 Formato esperado
Asunto: [Texto corto y claro]
Cuerpo: [Mensaje completo en párrafos breves]

---

## 📌 Ejemplos

### 1. Recepción (info parcial)

**Input:** Usuario reporta "no puedo acceder a la plataforma".  

**Output:**
Asunto: Hemos recibido tu reporte de acceso
Cuerpo: Hola, gracias por contactarnos. Hemos recibido tu reporte sobre el acceso a la plataforma.
Para poder ayudarte mejor, ¿puedes confirmarnos tu nombre de usuario y el navegador/dispositivo que usas?
Con esa información podremos avanzar en la revisión.

---

### 2. Diagnóstico (causa identificada)

**Input:** Causa → "error en servidor de autenticación", mitigación en curso.  

**Output:**
Asunto: Avance en el diagnóstico de tu caso
Cuerpo: Hola, hemos identificado que la dificultad para acceder se debe a un error temporal en nuestro servidor de autenticación.
Nuestro equipo ya está aplicando medidas de mitigación y esperamos una mejora en las próximas horas.
Te mantendremos informado con la siguiente actualización.

---

### 3. Resolución (problema solucionado)

**Input:** Acciones → "reinicio del servidor y ajuste en configuración".  

**Output:**
Asunto: Tu caso ha sido resuelto
Cuerpo: Hola, queremos informarte que tu caso fue resuelto.
Se realizaron las siguientes acciones: reinicio del servidor y ajuste en la configuración de autenticación.
Puedes validar intentando nuevamente el acceso.
Por favor, confírmanos si todo funciona correctamente para proceder con el cierre del caso.

---
