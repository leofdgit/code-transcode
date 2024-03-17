FROM python

# Create a non-root user
RUN adduser --system --no-create-home nonroot

# Set the working directory
WORKDIR /home/nonroot

COPY --chown=reguser:reguser runners/python/dag.py /home/nonroot/dag.py
COPY --chown=reguser:reguser runners/python/requirements.txt /home/nonroot/requirements.txt
COPY --chown=reguser:reguser output.py /home/nonroot/output.py
COPY --chown=reguser:reguser runners/python/runner.py /home/nonroot/runner.py
COPY --chown=reguser:reguser runners/python/runnerpy /home/nonroot/runner
COPY --chown=reguser:reguser runners/python/prepper /home/nonroot/prepper
COPY --chown=reguser:reguser _run.sh /home/nonroot/run.sh
COPY --chown=reguser:reguser test_cases.dat /home/nonroot/test_cases.dat

# Install deps
RUN python -m pip install -r requirements.txt

# USER nonroot
CMD ["/bin/bash", "run.sh"]