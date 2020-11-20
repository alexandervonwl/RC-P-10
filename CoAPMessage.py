class CoAPMessage:

    HEADER_LEN = 4
    VERSION = 0x1E
    MSG_TYPE = 0x1C
    TOKEN_LENGTH = 0x18
    MSG_CLASS = 0x15
    MSG_CODE = 0x10
    MSG_ID = 0x00

    def __init__(self, payload: str, msg_type: int, msg_class: int, msg_code: int, msg_id: int,
                 header_version=0x1, token_length=0x0, token=0x0):
        self.payload = payload
        self.header_version = header_version
        self.msg_type = msg_type
        self.token_length = token_length
        self.msg_class = msg_class
        self.msg_code = msg_code
        self.msg_id = msg_id
        self.token = token

    def __str__(self):
        return f"""[HEADER]: {self.header_version}, [TYPE]: {self.msg_type}, [TOKEN LENGTH]: {self.token_length}, \
[CLASS]: {self.msg_class}, [CODE]: {self.msg_code}, [ID]: {self.msg_id}
[TOKEN]: {hex(self.token) if self.token_length else ''}
[DATA]: {self.payload}\n"""

    def from_bytes(data_bytes: bytes):
        header_bytes = data_bytes[0:4]
        header_version = (0xC0 & header_bytes[0]) >> 6
        msg_type = (0x30 & header_bytes[0]) >> 4
        token_length = (0x0F & header_bytes[0]) >> 0
        msg_class = (header_bytes[1] >> 5) & 0x07
        msg_code = (header_bytes[1] >> 0) & 0x1F
        msg_id = (header_bytes[2] << 8) | header_bytes[3]
        if header_version != 0x1:
            raise ("Incorrect CoAP header version")
        elif 9 <= token_length <= 15:
            raise ("Incorrect CoAP token length")
        elif msg_class in (1, 6, 7):
            raise ("Message uses reserved CoAP message class")
        if (msg_class == 0x0 and msg_code == 0x0) or msg_type == 0x3:
            if not CoAPMessage.is_empty(msg_class, msg_code, token_length, data_bytes):
                raise ("Incorrect format for EMPTY CoAP message")
            if msg_type == 0x1:
                raise ("Non-confirmable CoAP message cannot be EMPTY")
        token = 0x0
        if token_length:
            token = int.from_bytes(data_bytes[4:4 + token_length], 'big')
        payload = data_bytes[5 + token_length:].decode('utf-8')
        return CoAPMessage(payload, msg_type, msg_class, msg_code, msg_id, header_version=header_version, token_length=token_length, token=token)

    def wrap(self) -> bytes:
        coap_header = self.build_header()
        payload = 0xFF.to_bytes(1, 'big') + self.payload.encode('utf-8')
        return coap_header.to_bytes(CoAPMessage.HEADER_LEN + self.token_length, 'big') + payload

    def build_header(self) -> int:
        header = 0x00
        header |= self.header_version << CoAPMessage.VERSION
        header |= (0b11 & self.msg_type) << CoAPMessage.MSG_TYPE
        header |= self.token_length << CoAPMessage.TOKEN_LENGTH
        header |= (0b111 & self.msg_class) << CoAPMessage.MSG_CLASS
        header |= (0x1F & self.msg_code) << CoAPMessage.MSG_CODE
        header |= (0xFFFF & self.msg_id) << CoAPMessage.MSG_ID
        if self.token_length:
            header = (header << 8 * self.token_length) | self.token
        return header

    def is_empty(msg_class: int, msg_code: int, token_length: int, data_bytes: bytes) -> bool:
        return msg_class == 0x0 and msg_code == 0x0 and token_length == 0x0 and len(data_bytes) == 4