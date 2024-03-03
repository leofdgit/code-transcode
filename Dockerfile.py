FROM python

# Create a non-root user
RUN adduser --system --no-create-home nonroot

# Set the working directory
WORKDIR /home/nonroot

COPY --chown=reguser:reguser output.py /home/nonroot/output.py
COPY --chown=reguser:reguser runner.py /home/nonroot/runner.py
COPY --chown=reguser:reguser runnerpy /home/nonroot/runner
COPY --chown=reguser:reguser _run.sh /home/nonroot/run.sh
COPY --chown=reguser:reguser test_cases.dat /home/nonroot/test_cases.dat

# USER nonroot
CMD ["/bin/bash", "run.sh"]