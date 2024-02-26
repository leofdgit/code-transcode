FROM node

# Create a non-root user
RUN adduser --system --no-create-home nonroot

# Set the working directory
WORKDIR /home/nonroot

COPY --chown=reguser:reguser output.js /home/nonroot/output.js
COPY --chown=reguser:reguser runner.js /home/nonroot/runner.js
COPY --chown=reguser:reguser runnerjs /home/nonroot/runner
COPY --chown=reguser:reguser _eval.sh /home/nonroot/eval.sh
COPY --chown=reguser:reguser test_cases.dat /home/nonroot/test_cases.dat

# USER nonroot
CMD ["/bin/bash", "eval.sh"]