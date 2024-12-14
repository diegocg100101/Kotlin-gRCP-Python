# Kotlin app and Python server | gRPC
 This is an implementation of gRPC between a Kotlin app (client) and Python (server)
 
 I found very little information when doing this practical implementation, the documentation of Google is poor, so I decided to publish this repository if it is usefull for someone else. First of all, and very important, the file build.gradle.kts has all the needed dependencies for protobuf and Kotlin Stub. This app simulates a very simple version of Uber, it only requires the X and Y position to simulate a trip, but the most important information about this implementation is how the stub codes are created and also how they are implemented to work with the Python server.
