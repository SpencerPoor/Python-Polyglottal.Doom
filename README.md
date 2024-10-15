# Python Polyglottal: 3D DOOM-Like Environment Program

This project is my personal exploration of the Python language and the RayLib graphics libraries used to create a fully functional 3D application made in the style of the DOOM video game's first person shooter layout.

This program's features include:
  - A fully 3D map
  - First person camera with mouse support for changing viewing angle
  - 3 degrees of freedom for movement (forward, backward, left, right)
  - Walls with collision and textures
  - Map overlay display toggle
      - Shows a top-down visual of currently rendered areas
  - Detailed notes alongside the written code explaining how every significant function works and how they enable the game's various features to work
   
This project is a useful exploration of data structures and how they can be applied to a 3D environment, particulary with how the "Binary Space Partitioning" data structure has been used to power the rendering methods of the original 90s DOOM video game, and how I could apply it to my own rendition of the game and understand how it works.

# How to run the program

## Method 1 **(Via IDE {VS Code, PyCharm etc.})**: Open the local repository install (Python-Polyglottal.Doom) in your IDE:

Ensure Python is installed in your IDE, or in the case of VS Code, install the Python extension from Microsoft

Open the main.py file, and run the file from within your IDE (often looks like a play button in the top right corner)

### **CONTROLS**:

**WASD** for movement

**MOUSE** for camera movement

**M** for top-down map overlay

**ESCAPE** to exit the program

## Method 2 **(Terminal)**: In a new terminal, type in the following:

MAKE SURE you have the latest version of Python installed to prevent issues

If you are not already in the local repository's main directory, navigate there:

```cd [Your cloned install location, should end in "Python-Polyglottal.Doom"]```

Once there, type in the following to execute the program:

```/usr/bin/python3 "./BSP_Engine/main.py"```

("/usr/bin/python3" is referring to the local python install location for python3, this is the default. If there are issues running this then either try again with your system's specific install path for python3 (or python) or refer to method 1 for the easier method)

### **CONTROLS**:

**WASD** for movement

**MOUSE** for camera movement

**M** for top-down map overlay

**ESCAPE** to exit the program