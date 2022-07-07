FROM gcc:latest
COPY . /usr/src/cppfiles
WORKDIR /usr/src/cppfiles
RUN g++ -o Test solution.cpp
CMD [ "./Test" ]

