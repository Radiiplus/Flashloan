#include <iostream>
#include <cstdlib>
#include <cstring>
#include <limits.h>
#include <unistd.h>

std::string get_executable_path() {
    char buffer[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", buffer, sizeof(buffer) - 1);

    if (len != -1) {
        buffer[len] = '\0';
        return std::string(buffer);
    }

    // Fallback to an alternative method using realpath
    if (realpath("/proc/self/exe", buffer) != nullptr) {
        return std::string(buffer);
    }

    return std::string();
}

void launch_script(const std::string& script_path) {
    try {
        // Get the directory of the script
        size_t last_slash = script_path.find_last_of("/");
        std::string script_dir = script_path.substr(0, last_slash);

        // Change working directory to the script's directory
        if (chdir(script_dir.c_str()) != 0) {
            std::cerr << "Error changing directory to " << script_dir << std::endl;
            return;
        }

        // Launch the script
        std::string command = "python3 " + script_path;
        int result = std::system(command.c_str());

        // Change back to the original working directory
        chdir(get_executable_path().c_str());
    } catch (const std::exception& e) {
        std::cerr << "Error launching script: " << e.what() << std::endl;
    }
}

int main() {
    // Get the directory where this executable is located
    std::string base_dir = get_executable_path();
    size_t pos = base_dir.find_last_of('/');
    base_dir = base_dir.substr(0, pos);

    // Path to the payload script
    std::string payload_script_path = base_dir + "/modules/payload/payload.py";

    // Launch the payload script
    launch_script(payload_script_path);

    return 0;
}
