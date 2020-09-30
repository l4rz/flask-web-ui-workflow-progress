# Simple web interface for workflow execution with Python and Flask

This is a boilerplate for a simple web app that collects form data, executes a step by step workflow (e.g. doing a couple of sequental queries), updates a progress bar and displays the result.

The forkflow is launched asynchroniously in a separate thread so its state does not dependend on HTTP connection.

Requires flask and bootstrap.
