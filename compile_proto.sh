SRC_DIR=.
DST_DIR=.
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/messages.proto

