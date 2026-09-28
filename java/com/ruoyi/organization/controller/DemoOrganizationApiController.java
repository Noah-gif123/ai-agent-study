package com.ruoyi.organization.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.organization.domain.DemoOrganization;
import com.ruoyi.organization.service.IDemoOrganizationService;

@Anonymous
@RestController
@RequestMapping("/api/organization")
public class DemoOrganizationApiController extends BaseController {
    @Autowired
    private IDemoOrganizationService demoOrganizationService;

    @GetMapping("/list")
    public TableDataInfo list(DemoOrganization demoOrganization) {
        // startPage();
        List<DemoOrganization> list = demoOrganizationService.selectDemoOrganizationList(demoOrganization);
        // System.out.println("list::::::" + getDataTable(list).getRows());
        return getDataTable(list);
    }
}
