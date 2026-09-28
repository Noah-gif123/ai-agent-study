package com.ruoyi.organization.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 机构管理对象 demo_organization
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
public class DemoOrganization extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 机构ID */
    private Long orgId;

    /** 机构类型 */
    @Excel(name = "机构类型")
    private Long orgType;

    /** 机构名称 */
    @Excel(name = "机构名称")
    private String orgName;

    /** 机构网址 */
    @Excel(name = "机构网址")
    private String orgWebsite;

    /** 创建用户ID */
    private Long createUserId;

    public void setOrgId(Long orgId) 
    {
        this.orgId = orgId;
    }

    public Long getOrgId() 
    {
        return orgId;
    }

    public void setOrgType(Long orgType) 
    {
        this.orgType = orgType;
    }

    public Long getOrgType() 
    {
        return orgType;
    }

    public void setOrgName(String orgName) 
    {
        this.orgName = orgName;
    }

    public String getOrgName() 
    {
        return orgName;
    }

    public void setOrgWebsite(String orgWebsite) 
    {
        this.orgWebsite = orgWebsite;
    }

    public String getOrgWebsite() 
    {
        return orgWebsite;
    }

    public void setCreateUserId(Long createUserId) 
    {
        this.createUserId = createUserId;
    }

    public Long getCreateUserId() 
    {
        return createUserId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("orgId", getOrgId())
            .append("orgType", getOrgType())
            .append("orgName", getOrgName())
            .append("orgWebsite", getOrgWebsite())
            .append("createUserId", getCreateUserId())
            .append("createTime", getCreateTime())
            .append("updateTime", getUpdateTime())
            .toString();
    }
}
