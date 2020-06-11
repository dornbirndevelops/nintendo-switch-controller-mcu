# generate bot script inputs for joining a sword and shield raid
# with every possible 4 digit input password

# for each password combination padding left 0
# create a file with a name indicating the current password combination

# then, write a series of start commands, which moves the bot to the position where
# the raid password is prompted.

# then enter the password according to the current combination

# finally enter the confirm command which submits the entered password

filename_prefix = 'enter_pw'

n = ''
w = '''0000088080808000 40
'''
e = '''0004088080808000 40
'''
l = '''0000080080808000 40
'''
r = '''000008ff80808000 40
'''
u = '''0000088000808000 40
'''
d = '''00000880ff808000 40
'''

commands_before = '''# initiate dialog
0004088080808000 50
# wait for choice box to come up
0000088080808000 380
# participate
0004088080808000 50
# to participate you need a password. continue?
0000088080808000 1200
# yes
0004088080808000 50
# connecting
0000088080808000 3200
# begin battle
0004088080808000 50
# wait for password input
0000088080808000 1000
# password input starts at 1. layout is as follows
# 1 2 3 delete
# 4 5 6 confirm
# 7 8 9 confirm
#   0   confirm
'''

commands_after = '''# confirm with +
0200088080808000 150

'''


move_commands = [
    # pos 0
    [
        # 0 (0)
        n,
        # 1 (0->8->5->4->1)
        u + w + u + l + u,
        # 2 (0->8->5->2)
        u + w + u + w + u,
        # 3 (0->8->5->6->3)
        u + w + u + r + u,
        # 4 (0->8->7->4)
        u + l + u,
        # 5 (0->8->5)
        u + w + u,
        # 6 (0->8->9->6)
        u + r + u,
        # 7 (0->8->7)
        u + l,
        # 8 (0->8)
        u,
        # 9 (0->8->9)
        u + r,
    ],
    # pos 1
    [
        # 0 (1->4->7->8->0)
        d + w + d + r + d,
        # 1 (1)
        n,
        # 2 (1->2)
        r,
        # 3 (1->2->3)
        r + w + r,
        # 4 (1->4)
        d,
        # 5 (1->2->5)
        r + d,
        # 6 (1->2->5->6)
        r + d + r,
        # 7 (1->4->7)
        d + w + d,
        # 8 (1->4->5->8)
        d + r + d,
        # 9 (1->2->5->6->9)
        r + d + r + d,
    ],
    # pos 2
    [
        # 0 (2->5->8->0)
        d + w + d + w + d,
        # 1 (2->1)
        l,
        # 2 (2)
        n,
        # 3 (2->3)
        r,
        # 4 (2->1->4)
        l + d,
        # 5 (2->5)
        d,
        # 6 (2->3->6)
        r + d,
        # 7 (2->5->4->7)
        d + l + d,
        # 8 (2->5->8)
        d + w + d,
        # 9 (2->5->6->9)
        d + r + d,
    ],
    # pos 3
    [
        # 0 (3->6->9->8->0)
        d + w + d + l + d,
        # 1 (3->2->1)
        l + w + l,
        # 2 (0->8->5->2)
        l,
        # 3 (0->8->5->6->3)
        n,
        # 4 (3->2->5->4)
        l + d + l,
        # 5 (3->2->5)
        l + d,
        # 6 (3->6)
        d,
        # 7 (3->2->5->4->7)
        l + d + l + d,
        # 8 (3->6->5->8)
        d + l + d,
        # 9 (3->6->9)
        d + w + d,
    ],
    # pos 4
    [
        # 0 (4->7->8->0)
        d + r + d,
        # 1 (4->1)
        u,
        # 2 (4->1->2)
        u + r,
        # 3 (4->5->2->3)
        r + u + r,
        # 4 (4)
        n,
        # 5 (4->5)
        r,
        # 6 (4->5->6)
        r + w + r,
        # 7 (4->7)
        d,
        # 8 (4->5->8)
        r + d,
        # 9 (4->5->8->9)
        r + d + r,
    ],
    # pos 5
    [
        # 0 (5->8->0)
        d + w + d,
        # 1 (5->2->1)
        u + l,
        # 2 (5->2)
        u,
        # 3 (5->2->3)
        u + r,
        # 4 (5->4)
        l,
        # 5 (5)
        n,
        # 6 (5->6)
        r,
        # 7 (5->4->7)
        l + d,
        # 8 (5->8)
        d,
        # 9 (5->6->9)
        r + d,
    ],
    # pos 6
    [
        # 0 (6->9->8->0)
        d + l + d,
        # 1 (6->5->2->1)
        l + u + l,
        # 2 (6->5->2)
        l + u,
        # 3 (6->3)
        u,
        # 4 (6->5->4)
        l + w + l,
        # 5 (6->5)
        l,
        # 6 (6)
        n,
        # 7 (6->5->8->7)
        l + d + l,
        # 8 (6->8)
        l + d,
        # 9 (6->9)
        d,
    ],
    # pos 7
    [
        # 0 (7->8->0)
        r + d,
        # 1 (7->4->1)
        u + w + u,
        # 2 (7->4->5->2)
        u + r + u,
        # 3 (7->8->5->6->3)
        r + u + r + u,
        # 4 (7->4)
        u,
        # 5 (7->8->5)
        r + u,
        # 6 (7->8->5->6)
        r + u + r,
        # 7 (77)
        n,
        # 8 (7->8)
        r,
        # 9 (7->8->9)
        r + w + r,
    ],
    # pos 8
    [
        # 0 (8->0)
        d,
        # 1 (8->5->4->1)
        u + l + u,
        # 2 (8->5->2)
        u + w + u,
        # 3 (8->5->6->3)
        u + r + u,
        # 4 (8->7->4)
        l + u,
        # 5 (8->5)
        u,
        # 6 (8->9->6)
        r + u,
        # 7 (8->7)
        l,
        # 8 (8)
        n,
        # 9 (8->9)
        r,
    ],
    # pos 9
    [
        # 0 (9->8->0)
        l + d,
        # 1 (9->8->5->4->1)
        l + u + l + u,
        # 2 (9->6->5->2)
        u + l + u,
        # 3 (9->6->3)
        u + w + u,
        # 4 (9->8->5->4)
        l + u + l,
        # 5 (9->8->5)
        l + u,
        # 6 (9->6)
        u,
        # 7 (9->8->7)
        l + w + l,
        # 8 (9->8)
        l,
        # 9 (9)
        n,
    ],
]


def move(pos, target, combination_idx):
    if pos == target and combination_idx:
        return w
    return move_commands[pos][target]


for i in range(10000):
    combination = f'{i:04}'
    pos = 1
    with open('{}_{}'.format(filename_prefix, combination), 'w') as file:
        file.write(commands_before)
        for j in range(len(combination)):
            target = int(combination[j])
            file.write('# from {} to {}\n'.format(pos, target))
            file.write(move(pos, target, j))
            pos = target
            file.write('# enter {} -> {}\n'.format(target, combination[:j+1]))
            file.write(e)
        file.write(commands_after)
