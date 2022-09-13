window.addEventListener("load", function () {
    "use strict";

    function sleep(s) {
        return new Promise((resolve) => setTimeout(resolve, s));
    }

    async function main() {
        let term;
        globalThis.pyodide = await loadPyodide({
            stdin: () => {
                let result = prompt();
                echo(result);
                return result;
            },
        });
        let init_namespace = pyodide.globals.get("dict")();

        pyodide.runPython(`
import sys
from pyodide.ffi import to_js
from pyodide.console import PyodideConsole, repr_shorten
import __main__

pyconsole = PyodideConsole(__main__.__dict__)
import builtins

async def await_fut(fut):
    res = await fut
    if res is not None:
        builtins._ = res
    return to_js([res], depth=1)
def clear_console():
    pyconsole.buffer = []

`,
            {globals: init_namespace}
        );


        let repr_shorten = init_namespace.get("repr_shorten");
        let await_fut = init_namespace.get("await_fut");
        let pyconsole = init_namespace.get("pyconsole");
        let clear_console = init_namespace.get("clear_console");
        const echo = (msg, ...opts) =>
            term.echo(
                msg
                    .replaceAll("]]", "&rsqb;&rsqb;")
                    .replaceAll("[[", "&lsqb;&lsqb;"),
                ...opts
            );

        init_namespace.destroy();

        term = $("#nsh");


        let ps1 = "nsh > ",
            ps2 = "  ... ";

        async function lock() {
            let resolve;
            let ready = term.ready;
            term.ready = new Promise((res) => (resolve = res));
            await ready;
            return resolve;
        }

        let public_namespace = pyodide.globals.get("dict")();

        public_namespace.set("__alert__", alert);
        public_namespace.set("__display__", document.getElementById("display"));

        pyodide.runPython(
            await (await fetch("./static/py/public.py")).text(),
            {globals: public_namespace}
        );

        async function interpreter(command) {
            let [cmd, cmd_args] = public_namespace.get("command_parser")(command);
            let is_command = public_namespace.get("command_checker")(cmd);

            if (is_command) {
                let ret = public_namespace.get("command_execute")(cmd, ...cmd_args);
                if(ret){
                    echo(ret);
                }
            } else {
                let unlock = await lock();
                term.pause();
                // multiline should be split (useful when pasting)
                for (const c of command.split("\n")) {
                    let fut = pyconsole.push(c);
                    term.set_prompt(fut.syntax_check === "incomplete" ? ps2 : ps1);
                    switch (fut.syntax_check) {
                        case "syntax-error":
                            term.error(fut.formatted_error.trimEnd());
                            continue;
                        case "incomplete":
                            continue;
                        case "complete":
                            break;
                        default:
                            throw new Error(`Unexpected type ${ty}`);
                    }
                    // In JavaScript, await automatically also awaits any results of
                    // awaits, so if an async function returns a future, it will await
                    // the inner future too. This is not what we want so we
                    // temporarily put it into a list to protect it.
                    let wrapped = await_fut(fut);
                    // complete case, get result / error and print it.

                    try {
                        let [value] = await wrapped;
                        if (value !== undefined) {
                            echo(
                                repr_shorten.callKwargs(value, {
                                    separator: "\n<long output truncated>\n",
                                })
                            );
                        }
                        if (pyodide.isPyProxy(value)) {
                            value.destroy();
                        }
                    } catch (e) {
                        if (e.constructor.name === "PythonError") {
                            const message = fut.formatted_error || e.message;
                            term.error(message.trimEnd());
                        } else {
                            throw e;
                        }
                    } finally {
                        fut.destroy();
                        wrapped.destroy();
                    }
                }
                term.resume();
                await sleep(10);
                unlock();
            }
            ;
        }

        term = term.terminal(interpreter, {
            greetings: "Welcome to nsh terminal.",
            prompt: ps1,
            completionEscape: false,
            completion: function (command, callback) {
                callback(pyconsole.complete(command).toJs()[0]);
            },
            keymap: {
                "CTRL+C": async function (event, original) {
                    clear_console();
                    term.enter();
                    echo("KeyboardInterrupt");
                    term.set_command("");
                    term.set_prompt(ps1);
                },
                "SHIFT+ENTER": (event, original) => {
                    return original(event);
                },
                TAB: (event, original) => {
                    const command = term.before_cursor();
                    // Disable completion for whitespaces.
                    if (command.trim() === "") {
                        term.insert("  ");
                        return false;
                    }
                    return original(event);
                },
            },
        });


        window.term = term;

        pyconsole.stdout_callback = (s) => echo(s, {newline: false});
        pyconsole.stderr_callback = (s) => {
            term.error(s.trimEnd());
        };
        term.ready = Promise.resolve();


        pyodide._api.on_fatal = async (e) => {
            term.error(
                "Pyodide has suffered a fatal error. Please report this to the Pyodide maintainers."
            );
            term.error("The cause of the fatal error was:");
            term.error(e);
            term.error("Look in the browser console for more details.");
            await term.ready;
            term.pause();
            await sleep(10);
            term.pause();
        };

        const searchParams = new URLSearchParams(window.location.search);
        if (searchParams.has("noblink")) {
            $(".cmd-cursor").addClass("noblink");
        }
    }

    $('.shell').resizable({
        minHeight: window.innerHeight * 0.1,
        minWidth: window.innerWidth * 0.33
    }).draggable({
        handle: '> .status-bar .title'
    });

    window.console_ready = main();
});
