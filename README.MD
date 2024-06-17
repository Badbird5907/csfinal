# CS Final Project
idk what to name this game so its Otter Game

# Dependencies
 - Windows
 - Minim

# Running
Either open final.pyde in processing3, or run the compiler:
`java -jar ProcessingCompiler.jar -o final.pyde -l`

`-o` = output file
`-l` = launch processing (omit if you are running through processing ide)

# Running with compiler
Java 17 or above is required. [Download](https://www.azul.com/downloads/?version=java-17-lts&os=windows&architecture=x86-64-bit&package=jdk#zulu)


**Installation Video:** https://youtu.be/DnhnucgBqzk


There should be a `config.json` file in the same directory as the compiler jar file.
Example:
```json
{
  "processingInstallPath": "C:\\Program Files\\Processing",
  "processingPyJarPath": "C:\\Program Files\\Processing\\py\\processing-py.jar"
}
```

The install path should be the install path of processing (the folder containing the processing exe)

The Python jar path should point to the path to the jar file of jycessing. (processing-py.jar)
Can be downloaded here: https://cdn.badbird.dev/temp/school/processing.py-windows64.zip or https://web.archive.org/web/20210117215614/https://py.processing.org/processing.py-windows64.zip (slower)


# Compiler
Download & Source: https://github.com/Badbird5907/ProcessingCompiler/releases/
