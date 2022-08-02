import os
import torch
import torchvision
from torchvision import transforms
from easydict import EasyDict

imagesize = 224

transform_test = transforms.Compose([
    transforms.Resize((imagesize, imagesize)),
    transforms.CenterCrop(imagesize),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_train = transforms.Compose([
    transforms.RandomCrop(imagesize, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_train_largescale = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

transform_test_largescale = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

transform_train_mnist = transforms.Compose([
    transforms.Resize(224),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

transform_fashion = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.3201, 0.3182, 0.3629), (0.1804, 0.3569, 0.1131))
])

transform_cifar10 = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.4881, 0.4660, 0.3994), (0.2380, 0.2322, 0.2413))
])

transform_sen12ms = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.1674, 0.1735, 0.2059), (0.1512, 0.1152, 0.1645))
])

transform_so2sat = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.2380, 0.3153, 0.5004), (0.0798, 0.1843, 0.0666))
])

kwargs = {'num_workers': 2, 'pin_memory': True}

def get_loader_in(args, config_type='default', split=('train', 'val')):
    config = EasyDict({
        "default": {
            'transform_train': transform_train,
            'transform_test': transform_test,
            'batch_size': args.batch_size,
            'transform_test_largescale': transform_test_largescale,
            'transform_train_largescale': transform_train_largescale,
            'transform_train_mnist': transform_train_largescale,
            'transform_sen12ms': transform_sen12ms,
            'transform_fashion': transform_fashion,
            'transform_cifar10': transform_cifar10,
            'transform_so2sat': transform_so2sat
        },
    })[config_type]

    train_loader, val_test_loader, lr_schedule, num_classes = None, None, [50, 75, 90], 0
    if args.in_dataset == "CIFAR-10":
        # Data loading code
        if 'train' in split:
            trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=config.transform_train)
            train_loader = torch.utils.data.DataLoader(trainset, batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            valset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
            val_test_loader = torch.utils.data.DataLoader(valset, batch_size=config.batch_size, shuffle=True, **kwargs)
        num_classes = 10
    elif args.in_dataset == "CIFAR-100":
        # Data loading code
        if 'train' in split:
            trainset = torchvision.datasets.CIFAR100(root='./data', train=True, download=True, transform=config.transform_train)
            train_loader = torch.utils.data.DataLoader(trainset, batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            valset = torchvision.datasets.CIFAR100(root='./data', train=False, download=True, transform=config.transform_test)
            val_test_loader = torch.utils.data.DataLoader(valset, batch_size=config.batch_size, shuffle=True, **kwargs)
        num_classes = 100
    elif args.in_dataset == "imagenet":
        root = os.path.join("datasets", "id_data", "imagenet")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_train_largescale),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_test_largescale),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        num_classes = 1000
    elif args.in_dataset == "rsicd_in":
        root = os.path.join("datasets", "id_data", "rsicd_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_train),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_test),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_test),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 23
    elif args.in_dataset == "mnist_fashion_in":
        root = os.path.join("datasets", "id_data", "mnist_fashion_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_fashion),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_fashion),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_fashion),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 7
    elif args.in_dataset == "xView2_in":
        root = os.path.join("datasets", "id_data", "xview2_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_train),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_test),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_test),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 7
    elif args.in_dataset == "rice_in":
        root = os.path.join("datasets", "id_data", "rice_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_train),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_test),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        num_classes = 3
    elif args.in_dataset == "sen12ms_in":
        root = os.path.join("datasets", "id_data", "sen12ms_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_sen12ms),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_sen12ms),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_sen12ms),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 9
    elif args.in_dataset == "cifar10_in":
        root = os.path.join("datasets", "id_data", "cifar10_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_cifar10),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_cifar10),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_cifar10),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 6
    elif args.in_dataset == "so2sat_in":
        root = os.path.join("datasets", "id_data", "so2sat_in")
        # Data loading code
        if 'train' in split:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'train'), config.transform_so2sat),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        if 'val' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'val'), config.transform_so2sat),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        if 'test' in split:
            val_test_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(root, 'test'), config.transform_so2sat),
                batch_size=config.batch_size, shuffle=False, **kwargs)
        num_classes = 10

    return EasyDict({
        "train_loader": train_loader,
        "val_test_loader": val_test_loader,
        "lr_schedule": lr_schedule,
        "num_classes": num_classes,
    })

def get_loader_out(args, dataset=(''), config_type='default', split=('train', 'val')):

    config = EasyDict({
        "default": {
            'transform_train': transform_train,
            'transform_test': transform_test,
            'transform_test_largescale': transform_test_largescale,
            'transform_train_largescale': transform_train_largescale,
            'transform_sen12ms': transform_sen12ms,
            'batch_size': args.batch_size
        },
    })[config_type]
    train_ood_loader, val_ood_loader = None, None

    if 'train' in split:
        if dataset[0].lower() == 'imagenet':
            train_ood_loader = torch.utils.data.DataLoader(
                ImageNet(transform=config.transform_train),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        elif dataset[0].lower() == 'tim':
            train_ood_loader = torch.utils.data.DataLoader(
                TinyImages(transform=config.transform_train),
                batch_size=config.batch_size, shuffle=True, **kwargs)

    if 'val' in split:
        val_dataset = dataset[1]
        batch_size = args.batch_size
        if val_dataset == 'SVHN':
            from util.svhn_loader import SVHN
            val_ood_loader = torch.utils.data.DataLoader(SVHN('datasets/ood_data/svhn/', split='test', transform=transform_test, download=False),
                                                       batch_size=batch_size, shuffle=False,
                                                        num_workers=2)
        elif val_dataset == 'dtd':
            transform = config.transform_test_largescale if args.in_dataset in {'imagenet'} else config.transform_test
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(root=os.path.join("datasets", "ood_data", "dtd", "images"), transform=transform),
                                                       batch_size=batch_size, shuffle=True, num_workers=2)
        elif val_dataset == 'CIFAR-100':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.CIFAR100(root='./data', train=False, download=True, transform=transform_test),
                                                       batch_size=batch_size, shuffle=True, num_workers=2)
        elif val_dataset == 'places50':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", "Places").format(val_dataset),
                                                          transform=config.transform_test_largescale), batch_size=batch_size, shuffle=False, num_workers=2)
        elif val_dataset == 'sun50':
            val_ood_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", "SUN"),
                                                 transform=config.transform_test_largescale), batch_size=batch_size, shuffle=False,
                num_workers=2)
        elif val_dataset == 'inat':
            val_ood_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", "iNaturalist"),
                                                 transform=config.transform_test_largescale), batch_size=batch_size, shuffle=False,
                num_workers=2)
        elif val_dataset == 'imagenet':
            val_ood_loader = torch.utils.data.DataLoader(
                torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "id_data", "imagenet", "val"), config.transform_test_largescale),
                batch_size=config.batch_size, shuffle=True, **kwargs)
        elif val_dataset == 'sen12ms_out':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", val_dataset),
                                                         transform=transform_sen12ms), batch_size=batch_size, shuffle=False, num_workers=2)
        elif val_dataset == 'so2sat_out':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", val_dataset),
                                                         transform=transform_so2sat), batch_size=batch_size, shuffle=False, num_workers=2)
        elif val_dataset == 'mnist_fashion_out':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", val_dataset),
                                                         transform=transform_fashion), batch_size=batch_size, shuffle=False, num_workers=2)
        elif val_dataset == 'cifar10_out':
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", val_dataset),
                                                         transform=transform_cifar10), batch_size=batch_size, shuffle=False, num_workers=2)
        else:
            val_ood_loader = torch.utils.data.DataLoader(torchvision.datasets.ImageFolder(os.path.join(".", "datasets", "ood_data", val_dataset),
                                                         transform=transform_test), batch_size=batch_size, shuffle=False, num_workers=2)

    return EasyDict({
        "train_ood_loader": train_ood_loader,
        "val_ood_loader": val_ood_loader,
    })