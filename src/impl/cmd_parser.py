#coding=utf8


def parse_args(input)  :
    status = parse_status()
    args = {}
    key  = None
    val  = None
    input += status.tag_sep
    status.to_unknow()
    for c in input :
        if status.is_quote():
            if c == status.tag_quote :
                status.to_back()
                continue
            status.append(c)
        if status.is_empty() :
            if c == status.tag_sep :
                continue
        if status.is_unknow():
            if c == status.tag_arg :
                status.to_arg_key()
                continue
            if c == status.tag_sep :
                continue
        if status.is_arg_key() :
            if c == status.tag_arg:
                status.mode_arg_long = True
                continue
            if status.mode_arg_long :
                end = False
                if c == status.tag_ass :
                    status.to_arg_val()
                    end = True
                if c == status.tag_sep or end :
                    key = status.target
                    args[key] = None
                    status.target = ""
                    status.to_arg_val()
                    continue
            else :
                if c == status.tag_sep  :
                    key = status.target
                    args[key] = None
                    status.target = ""
                    status.to_arg_val()
                    continue
            status.append(c)
        if status.is_arg_val() :
            if c == status.tag_quote :
                status.to_quote()
                continue
            if c == status.tag_sep :
                val       = status.target
                args[key] = val
                status.target = ""
                status.to_unknow()
                continue
            status.append(c)
    return args

def parse(input,cmder):
    status = parse_status()

    cmds = []
    args = {}
    key  = None
    val  = None
    input += status.tag_sep
    status.to_unknow()
    #import pdb
    #pdb.set_trace()
    for c in input :
        if status.is_quote():
            if c == status.tag_quote :
                status.append(c)
                status.to_back()
                continue
            status.append(c)
        if status.is_empty() :
            if c == status.tag_sep :
                continue
        if status.is_unknow():
            if c == status.tag_arg :
                status.to_arg_key()
                continue
            if c == status.tag_sep :
                continue
            status.to_cmd()
        if status.is_cmd() :
            if c == status.tag_sep :
                cmds.append(status.target)
                status.target = ""
                status.cur_mode = parse_status.mode_unknow
                status.to_unknow()
                continue
            else :
                status.append(c)
            pass
        if status.is_arg_key() :
            if c == status.tag_arg:
                status.mode_arg_long = True
                continue
            if status.mode_arg_long :
                end = False
                if c == status.tag_ass :
                    status.to_arg_val()
                    end = True
                if c == status.tag_sep or end :
                    key = status.target
                    status.target = ""
                    continue
            else :
                if c == status.tag_sep  :
                    key = status.target
                    status.target = ""
                    status.to_arg_val()
                    continue
            status.append(c)
        if status.is_arg_val() :
            if c == status.tag_quote :
                status.append(c)
                status.to_quote()
                continue
            if c == status.tag_sep :
                val = status.target
                if len(val.strip(status.tag_sep)) > 0 :
                    args[key] = val
                    status.target = ""
                    status.to_unknow()
                continue
            status.append(c)
    cmder.cmds = cmds
    cmder.args = args
    return


class parse_status:
    tag_sep = " "
    tag_ass = "="
    tag_arg = "-"
    tag_quote ='"'
    mode_arg_long   = False
    mode_cmd        = 1
    mode_arg_key    = 2
    mode_arg_val    = 3
    mode_unknow     = 4
    mode_quote      = 5
    pre_mode        = None
    cur_mode        = 0
    target          = ""
    def is_cmd(self)  :
        return self.cur_mode == self.mode_cmd
    def to_cmd(self)  :
        self.cur_mode = self.mode_cmd
    def is_unknow(self) :
        return self.cur_mode == self.mode_unknow
    def to_unknow(self) :
        self.cur_mode = self.mode_unknow
    def is_quote(self)  :
        return self.cur_mode == self.mode_quote

    def to_quote(self) :
        self.pre_mode = self.cur_mode
        self.cur_mode = self.mode_quote
    def to_back(self) :
        self.cur_mode = self.pre_mode
        self.pre_mode = None

    def is_arg_key(self):
        return self.cur_mode == self.mode_arg_key

    def is_arg_val(self):
        return self.cur_mode == self.mode_arg_val

    def to_arg_key(self):
        self.cur_mode = self.mode_arg_key
    def to_arg_val(self):
        self.cur_mode = self.mode_arg_val
    def is_empty(self):
        return len(self.target)  == 0
    def append(self,c) :
        self.target += c
    pass
