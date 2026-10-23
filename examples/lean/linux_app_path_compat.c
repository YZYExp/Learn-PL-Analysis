/* Optional Linux launcher compatibility adapter.
 * Some managed runtimes expose /proc/self/exe but reject /proc/<own-pid>/exe.
 * Lean 4.19.0's runtime uses the latter to locate its executable.
 * Only that exact current-process path is redirected; all other calls pass
 * through. No Lean code, theorem, tactic, or kernel operation is changed.
 * Build: cc -shared -fPIC linux_app_path_compat.c -o compat.so -ldl
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
    readlink_fn original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (!original) { errno = ENOSYS; return -1; }
    char own_executable[64];
    snprintf(own_executable, sizeof own_executable, "/proc/%ld/exe", (long)getpid());
    return original(strcmp(path, own_executable) == 0 ? "/proc/self/exe" : path,
                    buffer, size);
}
